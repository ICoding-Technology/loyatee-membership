from app.controllers.errors import BadRequest, Conflict, NotFound
from app.models import member


def list_members():
    return member.list_all()


def create_member(data):
    data = data or {}
    phone = data.get("phone")
    if not phone:
        raise BadRequest("phone is required")

    if member.find_by_phone(phone):
        raise Conflict("member already exists")

    return member.create(data)


def get_member(member_id):
    doc = member.find_by_id(member_id)
    if not doc:
        raise NotFound("member not found")
    return member.serialize(doc)


def update_member(member_id, data):
    updated = member.update(member_id, data or {})
    if not updated:
        raise NotFound("member not found")
    return updated


def delete_member(member_id):
    if not member.delete(member_id):
        raise NotFound("member not found")
    return {"message": "deleted"}
