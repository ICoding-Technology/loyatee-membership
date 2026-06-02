from app.controllers.errors import BadRequest, Conflict, NotFound
from app.models import store


def list_stores():
    return store.list_all()


def create_store(data):
    data = data or {}
    if not data.get("name"):
        raise BadRequest("name is required")
    slug = data.get("slug")
    if slug and store.find_by_slug(slug):
        raise Conflict("store slug already exists")
    return store.create(data)


def get_store(store_id):
    doc = store.find_by_id(store_id)
    if not doc:
        raise NotFound("store not found")
    return store.serialize(doc)


def resolve_store(token):
    """Public store info for a base64 subscribe token (no auth required)."""
    if not token:
        raise BadRequest("token is required")
    store_uuid = store.decode_token(token)
    if not store_uuid:
        raise BadRequest("invalid store token")
    doc = store.find_by_uuid(store_uuid)
    if not doc:
        raise NotFound("store not found")
    return store.serialize(doc)


def update_store(store_id, data):
    updated = store.update(store_id, data or {})
    if not updated:
        raise NotFound("store not found")
    return updated


def delete_store(store_id):
    if not store.delete(store_id):
        raise NotFound("store not found")
    return {"message": "deleted"}
