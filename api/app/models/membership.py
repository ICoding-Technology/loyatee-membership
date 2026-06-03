from datetime import datetime, timedelta

from app.extensions import get_db

COLLECTION = "memberships"


def _now():
    return datetime.utcnow().isoformat()


def _compute_expires_at(joined_at_iso, duration_days):
    """expires_at = joined_at + duration_days. None duration → never expires."""
    if not duration_days or duration_days <= 0:
        return None
    return (datetime.fromisoformat(joined_at_iso) + timedelta(days=duration_days)).isoformat()


def _full_id(collection, key):
    """Accept either a bare _key or an already-qualified id."""
    return key if "/" in str(key) else f"{collection}/{key}"


def _serialize(doc, points=None):
    if not doc:
        return None
    result = {
        "id": doc.get("_key"),
        "member_id": doc.get("_from"),
        "store_id": doc.get("_to"),
        "membership_no": doc.get("membership_no"),
        "tier": doc.get("tier"),
        "status": doc.get("status", "active"),
        "current_period": doc.get("current_period", 1),
        "period_started_at": doc.get("period_started_at"),
        "joined_at": doc.get("joined_at"),
        "expires_at": doc.get("expires_at"),  # null = never expires
        "is_expired": _is_expired(doc.get("expires_at")),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
    }
    if points is not None:
        result["points"] = points
    return result


def _is_expired(expires_at):
    # ISO-8601 UTC strings (same format) compare lexicographically by time.
    return bool(expires_at and expires_at < _now())


def find(member_key, store_key):
    db = get_db()
    cursor = db.aql.execute(
        f"FOR e IN {COLLECTION} "
        "FILTER e._from == @from AND e._to == @to LIMIT 1 RETURN e",
        bind_vars={
            "from": _full_id("members", member_key),
            "to": _full_id("stores", store_key),
        },
    )
    docs = list(cursor)
    return docs[0] if docs else None


def find_by_id(membership_key):
    db = get_db()
    return db.collection(COLLECTION).get(membership_key)


def subscribe(member_key, store_key, tier=None):
    """Create the member→store edge. Returns None if already subscribed.

    expires_at is derived from the store's configurable membership_duration_days
    (null on the store → membership never expires)."""
    if find(member_key, store_key):
        return None
    db = get_db()
    now = _now()

    from app.models import store as store_model

    store_doc = store_model.find_by_id(store_key)
    expires_at = _compute_expires_at(
        now, (store_doc or {}).get("membership_duration_days")
    )

    doc = {
        "_from": _full_id("members", member_key),
        "_to": _full_id("stores", store_key),
        "tier": tier,
        "status": "active",
        "current_period": 1,
        "period_started_at": now,
        "joined_at": now,
        "expires_at": expires_at,
        "created_at": now,
        "updated_at": now,
    }
    doc = {k: v for k, v in doc.items() if v is not None}
    meta = db.collection(COLLECTION).insert(doc)
    doc["_key"] = meta["_key"]
    return _serialize(doc, points=0)


def delete(membership_key):
    """Remove the membership edge. Returns False if it doesn't exist."""
    db = get_db()
    collection = db.collection(COLLECTION)
    if not collection.get(membership_key):
        return False
    collection.delete(membership_key)
    return True


def list_for_member(member_key):
    """All stores a member is subscribed to, each with its current balance."""
    db = get_db()
    cursor = db.aql.execute(
        f"""
        FOR store, edge IN OUTBOUND @memberId {COLLECTION}
            LET points = FIRST(
                FOR t IN transactions
                    FILTER t.membership_id == edge._id
                        AND t.period == edge.current_period
                    COLLECT AGGREGATE
                        cr = SUM(t.side == "Cr" ? t.amount : 0),
                        dr = SUM(t.side == "Dr" ? t.amount : 0)
                    RETURN cr - dr
            )
            RETURN {{ edge: edge, store: store, points: points }}
        """,
        bind_vars={"memberId": _full_id("members", member_key)},
    )
    from app.models import store as store_model

    out = []
    for row in cursor:
        membership = _serialize(row["edge"], points=row["points"] or 0)
        membership["store"] = store_model.serialize(row["store"])
        out.append(membership)
    return out


def serialize(doc, points=None):
    return _serialize(doc, points=points)
