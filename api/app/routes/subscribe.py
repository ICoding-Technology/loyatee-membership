from flask import Blueprint, request, jsonify

from app.controllers import memberships_controller
from app.controllers.auth_controller import require_auth

subscribe_bp = Blueprint("subscribe", __name__)


@subscribe_bp.get("")
@require_auth
def subscribe():
    store_token = request.args.get("store")
    return jsonify(memberships_controller.subscribe_via_link(store_token))
