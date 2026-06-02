from flask import Blueprint, request, jsonify

from app.controllers import memberships_controller

subscribe_bp = Blueprint("subscribe", __name__)


@subscribe_bp.get("")
def subscribe():
    store_token = request.args.get("store")
    return jsonify(memberships_controller.subscribe_via_link(store_token))
