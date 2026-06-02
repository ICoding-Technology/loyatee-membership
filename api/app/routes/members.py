from flask import Blueprint, request, jsonify

from app.controllers import members_controller, memberships_controller

members_bp = Blueprint("members", __name__)


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
def list_member_stores(member_id):
    return jsonify(memberships_controller.list_member_stores(member_id))


@members_bp.get("/<member_id>/transactions")
def member_transactions(member_id):
    limit = request.args.get("limit", default=50, type=int)
    return jsonify(memberships_controller.member_transactions(member_id, limit=limit))


@members_bp.patch("/<member_id>")
def update_member(member_id):
    return jsonify(members_controller.update_member(member_id, request.get_json()))


@members_bp.delete("/<member_id>")
def delete_member(member_id):
    return jsonify(members_controller.delete_member(member_id))
