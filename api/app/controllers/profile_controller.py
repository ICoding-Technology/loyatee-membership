from flask import g

from app.controllers.errors import NotFound
from app.models import member, membership


def get_profile():
    """Profile of the authenticated member (set on g by require_auth)."""
    member_id = g.get("member_id")
    doc = member.find_by_id(member_id)
    if doc is None:
        raise NotFound("member not found")

    return {
        "member": member.serialize(doc),
        "memberships": membership.list_for_member(member_id),
    }
