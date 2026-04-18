import random

from app.controllers.errors import BadRequest, Unauthorized

_otp_store = {}


def request_otp(data):
    phone = (data or {}).get("phone")
    if not phone:
        raise BadRequest("phone is required")

    otp = f"{random.randint(0, 999999):06d}"
    _otp_store[phone] = otp
    return {"message": "OTP sent", "otp_debug": otp}


def verify_otp(data):
    data = data or {}
    phone = data.get("phone")
    otp = data.get("otp")
    if not phone or not otp:
        raise BadRequest("phone and otp are required")

    if _otp_store.get(phone) != otp:
        raise Unauthorized("invalid otp")

    _otp_store.pop(phone, None)
    return {"message": "verified", "token": "stub-token"}
