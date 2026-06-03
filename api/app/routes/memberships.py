from flask import Blueprint, request, jsonify

from app.controllers import memberships_controller
from app.controllers.auth_controller import require_auth

memberships_bp = Blueprint("memberships", __name__)


@memberships_bp.post("")
def subscribe():
    return jsonify(memberships_controller.subscribe(request.get_json())), 201


@memberships_bp.get("/<membership_id>")
def get_membership(membership_id):
    return jsonify(memberships_controller.get_membership(membership_id))


@memberships_bp.post("/<membership_id>/earn")
def earn(membership_id):
    return jsonify(memberships_controller.earn(membership_id, request.get_json()))


@memberships_bp.post("/<membership_id>/redeem")
def redeem(membership_id):
    return jsonify(memberships_controller.redeem(membership_id, request.get_json()))


@memberships_bp.get("/<membership_id>/transactions")
def history(membership_id):
    period = request.args.get("period", type=int)
    include_archive = request.args.get("include_archive") == "true"
    return jsonify(
        memberships_controller.history(
            membership_id, period=period, include_archive=include_archive
        )
    )


@memberships_bp.post("/<membership_id>/close")
def close(membership_id):
    return jsonify(memberships_controller.close(membership_id))


# Member-facing (ownership enforced in the controller via g.member_id).
@memberships_bp.post("/<membership_id>/redeem-reward")
@require_auth
def redeem_reward(membership_id):
    return jsonify(memberships_controller.redeem_reward(membership_id, request.get_json()))


@memberships_bp.delete("/<membership_id>")
@require_auth
def unsubscribe(membership_id):
    return jsonify(memberships_controller.unsubscribe(membership_id))
