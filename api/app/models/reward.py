from datetime import datetime

from app.extensions import get_db

COLLECTION = "rewards"


def _now():
    return datetime.utcnow().isoformat()


def _serialize(doc):
    if not doc:
        return None
    return {
        "id": doc.get("_key"),
        "store_id": doc.get("store_id"),
        "name": doc.get("name"),
        "description": doc.get("description"),
        "points_cost": doc.get("points_cost", 0),
        "status": doc.get("status", "active"),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
    }


def _store_id(store_key):
    return store_key if "/" in str(store_key) else f"stores/{store_key}"


def list_for_store(store_key, active_only=True):
    db = get_db()
    status_filter = 'FILTER r.status == "active"' if active_only else ""
    cursor = db.aql.execute(
        f"""
        FOR r IN {COLLECTION}
            FILTER r.store_id == @storeId {status_filter}
            SORT r.points_cost ASC
            RETURN r
        """,
        bind_vars={"storeId": _store_id(store_key)},
    )
    return [_serialize(d) for d in cursor]


def find_by_id(reward_id):
    db = get_db()
    return db.collection(COLLECTION).get(reward_id)


def create(store_key, data):
    db = get_db()
    now = _now()
    doc = {
        "store_id": _store_id(store_key),
        "name": data.get("name"),
        "description": data.get("description"),
        "points_cost": data.get("points_cost", 0),
        "status": data.get("status", "active"),
        "created_at": now,
        "updated_at": now,
    }
    doc = {k: v for k, v in doc.items() if v is not None}
    meta = db.collection(COLLECTION).insert(doc)
    doc["_key"] = meta["_key"]
    return _serialize(doc)


def update(reward_id, data):
    db = get_db()
    collection = db.collection(COLLECTION)
    if not collection.get(reward_id):
        return None
    allowed = ("name", "description", "points_cost", "status")
    patch = {k: v for k, v in data.items() if k in allowed}
    patch["updated_at"] = _now()
    patch["_key"] = reward_id
    collection.update(patch)
    return _serialize(collection.get(reward_id))


def delete(reward_id):
    db = get_db()
    collection = db.collection(COLLECTION)
    if not collection.get(reward_id):
        return False
    collection.delete(reward_id)
    return True


def serialize(doc):
    return _serialize(doc)
