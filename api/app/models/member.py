import random
from datetime import datetime

from app.extensions import get_db

COLLECTION = "members"

SIGNIN_TYPES = ("phone", "google", "telegram")


def _now():
    return datetime.utcnow().isoformat()


def _serialize(doc):
    if not doc:
        return None
    return {
        "id": doc.get("_key"),
        "account_id": doc.get("account_id"),
        "signin_type": doc.get("signin_type"),
        "phone": doc.get("phone"),
        "name": doc.get("name"),
        "email": doc.get("email"),
        "avatar_url": doc.get("avatar_url"),
        "google_id": doc.get("google_id"),
        "telegram_id": doc.get("telegram_id"),
        "points": doc.get("points", 0),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
    }


def _query_one(filter_clause, bind_vars):
    db = get_db()
    cursor = db.aql.execute(
        f"FOR m IN {COLLECTION} FILTER {filter_clause} LIMIT 1 RETURN m",
        bind_vars=bind_vars,
    )
    docs = list(cursor)
    return docs[0] if docs else None


def list_all():
    db = get_db()
    cursor = db.aql.execute(f"FOR m IN {COLLECTION} RETURN m")
    return [_serialize(d) for d in cursor]


def find_by_phone(phone):
    return _query_one("m.phone == @phone", {"phone": phone})


def find_by_google_id(google_id):
    return _query_one("m.google_id == @gid", {"gid": google_id})


def find_by_telegram_id(telegram_id):
    return _query_one("m.telegram_id == @tid", {"tid": telegram_id})


def find_by_email(email):
    return _query_one("m.email == @email", {"email": email})


def find_by_id(member_id):
    db = get_db()
    return db.collection(COLLECTION).get(member_id)


def find_by_account_id(account_id):
    return _query_one("m.account_id == @aid", {"aid": account_id})


def generate_account_id(max_attempts: int = 10) -> str:
    """Random unique 6-digit string. Retries on collision; raises after max_attempts."""
    for _ in range(max_attempts):
        candidate = f"{random.randint(100000, 999999)}"
        if find_by_account_id(candidate) is None:
            return candidate
    raise RuntimeError("could not allocate a unique account_id")


def _build_doc(data):
    now = _now()
    doc = {
        "account_id": data.get("account_id"),
        "signin_type": data.get("signin_type"),
        "phone": data.get("phone"),
        "name": data.get("name"),
        "email": data.get("email"),
        "avatar_url": data.get("avatar_url"),
        "google_id": data.get("google_id"),
        "telegram_id": data.get("telegram_id"),
        "points": data.get("points", 0),
        "created_at": now,
        "updated_at": now,
    }
    return {k: v for k, v in doc.items() if v is not None}


def create(data):
    db = get_db()
    payload = dict(data or {})
    if not payload.get("account_id"):
        payload["account_id"] = generate_account_id()
    doc = _build_doc(payload)
    if "created_at" not in doc:
        doc["created_at"] = _now()
        doc["updated_at"] = doc["created_at"]
    meta = db.collection(COLLECTION).insert(doc)
    doc["_key"] = meta["_key"]
    return _serialize(doc)


def update(member_id, data):
    db = get_db()
    collection = db.collection(COLLECTION)
    existing = collection.get(member_id)
    if not existing:
        return None
    allowed = ("name", "email", "avatar_url", "phone", "points")
    patch = {k: v for k, v in data.items() if k in allowed}
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
