from flask import Blueprint, jsonify

from app.controllers import profile_controller

profile_bp = Blueprint("profile", __name__)


@profile_bp.get("")
def get_profile():
    return jsonify(profile_controller.get_profile())
