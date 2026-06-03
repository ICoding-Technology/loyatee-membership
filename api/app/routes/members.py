from flask import Blueprint, request, jsonify

from app.controllers import members_controller, memberships_controller
from app.controllers.auth_controller import require_auth, require_self

members_bp = Blueprint("members", __name__)


# NOTE: list/create/get-by-id/delete below are an unauthenticated admin surface
# (no role model yet). The self-scoped endpoints are guarded with
# require_auth + require_self so a member can only touch their own record.
@members_bp.get("")
def list_members():
    return jsonify(members_controller.list_members())


@members_bp.post("")
def create_member():
    return jsonify(members_controller.create_member(request.get_json())), 201


@members_bp.get("/<member_id>")
def get_member(member_id):
    return jsonify(members_controller.get_member(member_id))


@members_bp.get("/<member_id>/stores")
@require_auth
@require_self
def list_member_stores(member_id):
    return jsonify(memberships_controller.list_member_stores(member_id))


@members_bp.get("/<member_id>/transactions")
@require_auth
@require_self
def member_transactions(member_id):
    limit = request.args.get("limit", default=50, type=int)
    return jsonify(memberships_controller.member_transactions(member_id, limit=limit))


@members_bp.patch("/<member_id>")
@require_auth
@require_self
def update_member(member_id):
    return jsonify(members_controller.update_member(member_id, request.get_json()))


@members_bp.delete("/<member_id>")
def delete_member(member_id):
    return jsonify(members_controller.delete_member(member_id))
