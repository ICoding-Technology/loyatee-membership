import base64
import uuid
from datetime import datetime

from app.extensions import get_db

COLLECTION = "stores"


def _now():
    return datetime.utcnow().isoformat()


def encode_token(store_uuid):
    """Public, link-safe handle for a store: base64(uuid). Never the _key."""
    if not store_uuid:
        return None
    return base64.urlsafe_b64encode(store_uuid.encode()).decode().rstrip("=")


def decode_token(token):
    """Reverse of encode_token. Returns the store uuid, or None if malformed."""
    if not token:
        return None
    try:
        padded = token + "=" * (-len(token) % 4)
        return base64.urlsafe_b64decode(padded.encode()).decode()
    except (ValueError, UnicodeDecodeError):
        return None


def _serialize(doc):
    if not doc:
        return None
    return {
        "id": doc.get("_key"),
        "uuid": doc.get("uuid"),
        "subscribe_token": encode_token(doc.get("uuid")),
        "slug": doc.get("slug"),
        "name": doc.get("name"),
        "logo_url": doc.get("logo_url"),
        "category": doc.get("category"),
        "status": doc.get("status", "active"),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
    }


def list_all():
    db = get_db()
    cursor = db.aql.execute(f"FOR s IN {COLLECTION} RETURN s")
    return [_serialize(d) for d in cursor]


def find_by_id(store_id):
    db = get_db()
    return db.collection(COLLECTION).get(store_id)


def find_by_slug(slug):
    db = get_db()
    cursor = db.aql.execute(
        f"FOR s IN {COLLECTION} FILTER s.slug == @slug LIMIT 1 RETURN s",
        bind_vars={"slug": slug},
    )
    docs = list(cursor)
    return docs[0] if docs else None


def find_by_uuid(store_uuid):
    db = get_db()
    cursor = db.aql.execute(
        f"FOR s IN {COLLECTION} FILTER s.uuid == @uuid LIMIT 1 RETURN s",
        bind_vars={"uuid": store_uuid},
    )
    docs = list(cursor)
    return docs[0] if docs else None


def create(data):
    db = get_db()
    now = _now()
    doc = {
        "uuid": uuid.uuid4().hex,
        "slug": data.get("slug"),
        "name": data.get("name"),
        "logo_url": data.get("logo_url"),
        "category": data.get("category"),
        "status": data.get("status", "active"),
        "created_at": now,
        "updated_at": now,
    }
    doc = {k: v for k, v in doc.items() if v is not None}
    meta = db.collection(COLLECTION).insert(doc)
    doc["_key"] = meta["_key"]
    return _serialize(doc)


def update(store_id, data):
    db = get_db()
    collection = db.collection(COLLECTION)
    if not collection.get(store_id):
        return None
    allowed = ("slug", "name", "logo_url", "category", "status")
    patch = {k: v for k, v in data.items() if k in allowed}
    patch["updated_at"] = _now()
    patch["_key"] = store_id
    collection.update(patch)
    return _serialize(collection.get(store_id))


def delete(store_id):
    db = get_db()
    collection = db.collection(COLLECTION)
    if not collection.get(store_id):
        return False
    collection.delete(store_id)
    return True


def serialize(doc):
    return _serialize(doc)
