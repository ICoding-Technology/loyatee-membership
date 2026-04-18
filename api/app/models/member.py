from datetime import datetime

from app.extensions import get_db

COLLECTION = "members"


def _now():
    return datetime.utcnow().isoformat()


def _serialize(doc):
    if not doc:
        return None
    return {
        "id": doc.get("_key"),
        "phone": doc.get("phone"),
        "name": doc.get("name"),
        "email": doc.get("email"),
        "points": doc.get("points", 0),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
    }


def list_all():
    db = get_db()
    cursor = db.aql.execute(f"FOR m IN {COLLECTION} RETURN m")
    return [_serialize(d) for d in cursor]


def find_by_phone(phone):
    db = get_db()
    cursor = db.aql.execute(
        f"FOR m IN {COLLECTION} FILTER m.phone == @phone LIMIT 1 RETURN m",
        bind_vars={"phone": phone},
    )
    docs = list(cursor)
    return docs[0] if docs else None


def find_by_id(member_id):
    db = get_db()
    doc = db.collection(COLLECTION).get(member_id)
    return doc


def create(data):
    db = get_db()
    now = _now()
    doc = {
        "phone": data["phone"],
        "name": data.get("name"),
        "email": data.get("email"),
        "points": data.get("points", 0),
        "created_at": now,
        "updated_at": now,
    }
    meta = db.collection(COLLECTION).insert(doc)
    doc["_key"] = meta["_key"]
    return _serialize(doc)


def update(member_id, data):
    db = get_db()
    collection = db.collection(COLLECTION)
    existing = collection.get(member_id)
    if not existing:
        return None
    patch = {k: v for k, v in data.items() if k in ("name", "email", "points")}
    patch["updated_at"] = _now()
    patch["_key"] = member_id
    collection.update(patch)
    return _serialize(collection.get(member_id))


def delete(member_id):
    db = get_db()
    collection = db.collection(COLLECTION)
    if not collection.get(member_id):
        return False
    collection.delete(member_id)
    return True


def serialize(doc):
    return _serialize(doc)
