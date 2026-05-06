from flask import Blueprint, request, jsonify

from app.controllers import auth_controller

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/request-otp")
def request_otp():
    return jsonify(auth_controller.request_otp(request.get_json()))


@auth_bp.post("/verify-otp")
def verify_otp():
    return jsonify(auth_controller.verify_otp(request.get_json()))


@auth_bp.post("/google")
def google_signin():
    return jsonify(auth_controller.google_signin(request.get_json()))


@auth_bp.post("/telegram")
def telegram_signin():
    return jsonify(auth_controller.telegram_signin(request.get_json()))
