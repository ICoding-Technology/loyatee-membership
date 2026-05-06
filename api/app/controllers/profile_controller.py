from flask import request

from app.controllers.auth_controller import parse_token
from app.controllers.errors import NotFound, Unauthorized
from app.models import member


def _bearer_token():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    return header[len("Bearer "):].strip() or None


def get_profile():
    token = _bearer_token()
    if not token:
        raise Unauthorized("missing bearer token")

    member_id = parse_token(token)
    if not member_id:
        raise Unauthorized("invalid token")

    doc = member.find_by_id(member_id)
    if doc is None:
        raise NotFound("member not found")

    return {"member": member.serialize(doc)}
