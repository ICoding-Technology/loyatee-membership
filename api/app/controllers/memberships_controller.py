from flask import g

from app.controllers.errors import BadRequest, Conflict, Forbidden, NotFound
from app.models import member, membership, reward, store, transaction


def _owned_membership(membership_id):
    """Load a membership and ensure it belongs to the authenticated member."""
    ms = membership.find_by_id(membership_id)
    if not ms:
        raise NotFound("membership not found")
    if ms.get("_from") != f"members/{g.get('member_id')}":
        raise Forbidden("not your membership")
    return ms


def subscribe(data):
    data = data or {}
    member_id = data.get("member_id")
    store_id = data.get("store_id")
    if not member_id or not store_id:
        raise BadRequest("member_id and store_id are required")
    if not member.find_by_id(member_id):
        raise NotFound("member not found")
    if not store.find_by_id(store_id):
        raise NotFound("store not found")

    result = membership.subscribe(member_id, store_id, tier=data.get("tier"))
    if result is None:
        raise Conflict("member already subscribed to this store")
    return result


def subscribe_via_link(store_token):
    """Subscribe the bearer-authenticated member to the store referenced by a
    base64-encoded public uuid (used for share links / QR codes). Idempotent:
    a repeat click returns the existing membership instead of erroring."""
    member_id = g.get("member_id")  # set by require_auth on the route
    if not member.find_by_id(member_id):
        raise NotFound("member not found")

    if not store_token:
        raise BadRequest("store is required")
    store_uuid = store.decode_token(store_token)
    if not store_uuid:
        raise BadRequest("invalid store token")
    store_doc = store.find_by_uuid(store_uuid)
    if not store_doc:
        raise NotFound("store not found")

    store_key = store_doc["_key"]
    result = membership.subscribe(member_id, store_key)
    if result is None:
        existing = membership.find(member_id, store_key)
        points = transaction.balance(existing["_key"])
        return membership.serialize(existing, points=points)
    return result


def list_member_stores(member_id):
    if not member.find_by_id(member_id):
        raise NotFound("member not found")
    return membership.list_for_member(member_id)


def member_transactions(member_id, limit=50):
    if not member.find_by_id(member_id):
        raise NotFound("member not found")
    return transaction.list_for_member(member_id, limit=limit)


def get_membership(membership_id):
    ms = membership.find_by_id(membership_id)
    if not ms:
        raise NotFound("membership not found")
    points = transaction.balance(membership_id)
    return membership.serialize(ms, points=points)


def earn(membership_id, data):
    data = data or {}
    amount = data.get("amount")
    if not isinstance(amount, int) or amount <= 0:
        raise BadRequest("amount must be a positive integer")
    result = transaction.earn(membership_id, amount, reference=data.get("reference"))
    if result is None:
        raise NotFound("membership not found")
    return result


def redeem(membership_id, data):
    data = data or {}
    amount = data.get("amount")
    if not isinstance(amount, int) or amount <= 0:
        raise BadRequest("amount must be a positive integer")
    result = transaction.redeem(membership_id, amount, reference=data.get("reference"))
    if result is None:
        raise NotFound("membership not found")
    if isinstance(result, dict) and result.get("error"):
        raise Conflict(result["error"])
    return result


def history(membership_id, period=None, include_archive=False):
    rows = transaction.history(
        membership_id, period=period, include_archive=include_archive
    )
    if rows is None:
        raise NotFound("membership not found")
    return rows


def close(membership_id):
    result = transaction.close_period(membership_id)
    if result is None:
        raise NotFound("membership not found")
    return result


def redeem_reward(membership_id, data):
    """Member redeems a reward: debits its points_cost from this membership."""
    ms = _owned_membership(membership_id)
    if membership._is_expired(ms.get("expires_at")):
        raise Conflict("membership has expired")

    reward_id = (data or {}).get("reward_id")
    if not reward_id:
        raise BadRequest("reward_id is required")
    reward_doc = reward.find_by_id(reward_id)
    if not reward_doc:
        raise NotFound("reward not found")
    if reward_doc.get("store_id") != ms.get("_to"):
        raise BadRequest("reward does not belong to this store")
    if reward_doc.get("status", "active") != "active":
        raise Conflict("reward is not available")

    cost = reward_doc.get("points_cost", 0)
    result = transaction.redeem(
        membership_id, cost, reference=f"reward:{reward_id}:{reward_doc.get('name')}"
    )
    if isinstance(result, dict) and result.get("error"):
        raise Conflict(result["error"])
    return {
        "message": "redeemed",
        "reward": reward.serialize(reward_doc),
        "transaction": result,
        "balance": transaction.balance(membership_id),
    }


def unsubscribe(membership_id):
    """Member leaves a store: removes the membership edge and its ledger."""
    _owned_membership(membership_id)
    transaction.delete_for_membership(membership_id)
    membership.delete(membership_id)
    return {"message": "unsubscribed"}
