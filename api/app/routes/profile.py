from flask import Blueprint, jsonify

from app.controllers import profile_controller
from app.controllers.auth_controller import require_auth

profile_bp = Blueprint("profile", __name__)


@profile_bp.get("")
@require_auth
def get_profile():
    return jsonify(profile_controller.get_profile())
