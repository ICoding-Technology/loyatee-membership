from datetime import datetime

from app.extensions import get_db
from app.models import membership as membership_model

COLLECTION = "transactions"
ARCHIVE = "transactions_archive"

# Accounting convention: points are credited (Cr) when earned and debited (Dr)
# when redeemed. The balance is always derived by summing the ledger — there is
# no mutable balance field — so concurrent earns are conflict-free appends.
CR = "Cr"
DR = "Dr"


def _now():
    return datetime.utcnow().isoformat()


def _period_balance(db, membership_id, period):
    cursor = db.aql.execute(
        f"""
        FOR t IN {COLLECTION}
            FILTER t.membership_id == @membershipId AND t.period == @period
            COLLECT AGGREGATE
                cr = SUM(t.side == "{CR}" ? t.amount : 0),
                dr = SUM(t.side == "{DR}" ? t.amount : 0)
            RETURN cr - dr
        """,
        bind_vars={"membershipId": membership_id, "period": period},
    )
    result = list(cursor)
    return result[0] if result and result[0] is not None else 0


def _serialize(doc):
    if not doc:
        return None
    return {
        "id": doc.get("_key"),
        "membership_id": doc.get("membership_id"),
        "member_id": doc.get("member_id"),
        "store_id": doc.get("store_id"),
        "period": doc.get("period"),
        "type": doc.get("type"),
        "side": doc.get("side"),
        "amount": doc.get("amount"),
        "reference": doc.get("reference"),
        "created_at": doc.get("created_at"),
    }


def balance(membership_key):
    """Current-period balance for a membership, or None if it doesn't exist."""
    ms = membership_model.find_by_id(membership_key)
    if not ms:
        return None
    db = get_db()
    return _period_balance(db, ms["_id"], ms.get("current_period", 1))


def _post(ms, side, amount, type_, reference):
    db = get_db()
    doc = {
        "membership_id": ms["_id"],
        "member_id": ms["_from"],
        "store_id": ms["_to"],
        "period": ms.get("current_period", 1),
        "type": type_,
        "side": side,
        "amount": amount,
        "reference": reference,
        "created_at": _now(),
    }
    doc = {k: v for k, v in doc.items() if v is not None}
    meta = db.collection(COLLECTION).insert(doc)
    doc["_key"] = meta["_key"]
    return _serialize(doc)


def earn(membership_key, amount, reference=None):
    """Credit points. A conflict-free append — safe under concurrency."""
    if amount <= 0:
        raise ValueError("earn amount must be positive")
    ms = membership_model.find_by_id(membership_key)
    if not ms:
        return None
    return _post(ms, CR, amount, "earn", reference)


def redeem(membership_key, amount, reference=None):
    """Debit points.

    The overdraw check below is NOT atomic — two concurrent redeems on the
    same membership could both pass it. A per-membership exclusive lock
    (stream transaction) will be added when the redeem flow is built out;
    until then callers should treat this as best-effort.
    """
    if amount <= 0:
        raise ValueError("redeem amount must be positive")
    ms = membership_model.find_by_id(membership_key)
    if not ms:
        return None
    db = get_db()
    current = _period_balance(db, ms["_id"], ms.get("current_period", 1))
    if current < amount:
        return {"error": "insufficient points", "balance": current}
    return _post(ms, DR, amount, "redeem", reference)


def list_for_member(member_key, limit=50):
    """Recent activity across all of a member's memberships, newest first,
    annotated with the store name. Excludes carry-forward 'opening' rows."""
    db = get_db()
    member_id = member_key if "/" in str(member_key) else f"members/{member_key}"
    cursor = db.aql.execute(
        f"""
        FOR t IN {COLLECTION}
            FILTER t.member_id == @memberId AND t.type != "opening"
            SORT t.created_at DESC
            LIMIT @limit
            LET store = DOCUMENT(t.store_id)
            RETURN MERGE(t, {{ store_name: store.name }})
        """,
        bind_vars={"memberId": member_id, "limit": limit},
    )
    out = []
    for doc in cursor:
        row = _serialize(doc)
        row["store_name"] = doc.get("store_name")
        out.append(row)
    return out


def history(membership_key, period=None, include_archive=False):
    ms = membership_model.find_by_id(membership_key)
    if not ms:
        return None
    db = get_db()
    sources = [COLLECTION, ARCHIVE] if include_archive else [COLLECTION]
    rows = []
    for source in sources:
        period_filter = "AND t.period == @period" if period is not None else ""
        bind_vars = {"membershipId": ms["_id"]}
        if period is not None:
            bind_vars["period"] = period
        cursor = db.aql.execute(
            f"""
            FOR t IN {source}
                FILTER t.membership_id == @membershipId {period_filter}
                SORT t.created_at DESC
                RETURN t
            """,
            bind_vars=bind_vars,
        )
        rows.extend(_serialize(d) for d in cursor)
    return rows


def close_period(membership_key):
    """Carry the running balance forward and archive the closed period.

    Folds every row of the current period into a single immutable 'opening'
    row in the next period, then moves the closed rows into the archive
    collection. This keeps the hot `transactions` collection — and therefore
    the balance SUM — bounded to roughly one period of activity. Idempotent:
    re-running after a close is a no-op.
    """
    ms = membership_model.find_by_id(membership_key)
    if not ms:
        return None

    db = get_db()
    membership_id = ms["_id"]
    period = ms.get("current_period", 1)
    next_period = period + 1
    now = _now()

    # No-op guard: only close a period that has real activity. A period
    # holding nothing but its carry-forward opening row has nothing to settle,
    # so repeated/accidental close calls don't inflate empty periods.
    activity = db.aql.execute(
        f"""
        FOR t IN {COLLECTION}
            FILTER t.membership_id == @membershipId
                AND t.period == @period AND t.type != "opening"
            LIMIT 1 RETURN 1
        """,
        bind_vars={"membershipId": membership_id, "period": period},
    )
    if not list(activity):
        return _serialize_close(membership_id, period, period, None)

    net = _period_balance(db, membership_id, period)

    opening = {
        "membership_id": membership_id,
        "member_id": ms["_from"],
        "store_id": ms["_to"],
        "period": next_period,
        "type": "opening",
        "side": CR if net >= 0 else DR,
        "amount": abs(net),
        "reference": "carry_forward",
        "created_at": now,
    }
    db.collection(COLLECTION).insert(opening)

    # Move the closed period's rows into the archive (preserve _key for audit).
    archived = db.aql.execute(
        f"""
        FOR t IN {COLLECTION}
            FILTER t.membership_id == @membershipId AND t.period == @period
            INSERT UNSET(t, "_id", "_rev") INTO {ARCHIVE}
            REMOVE t IN {COLLECTION}
            COLLECT WITH COUNT INTO n
            RETURN n
        """,
        bind_vars={"membershipId": membership_id, "period": period},
    )
    moved = next(iter(archived), 0)

    db.collection(membership_model.COLLECTION).update(
        {
            "_key": ms["_key"],
            "current_period": next_period,
            "period_started_at": now,
            "updated_at": now,
        }
    )
    return _serialize_close(membership_id, period, next_period, net, moved)


def _serialize_close(membership_id, period, next_period, net, archived=0):
    return {
        "membership_id": membership_id,
        "closed_period": period,
        "new_period": next_period,
        "carried_forward": net,
        "archived_rows": archived,
        "already_closed": net is None,
    }
