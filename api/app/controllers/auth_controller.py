import hashlib
import hmac
import json
import random
import time
import urllib.error
import urllib.request

from flask import current_app

from app.controllers.errors import BadRequest, Unauthorized
from app.extensions import get_redis
from app.models import member

TELEGRAM_GATEWAY_URL = "https://gatewayapi.telegram.org/sendVerificationMessage"


def _otp_key(phone: str) -> str:
    return f"otp:{phone}"


def _issue_token(member_id: str) -> str:
    # Stub token format until JWT is wired up. Profile endpoint parses the id back out.
    return f"stub:{member_id}"


def parse_token(token: str):
    if not token or not token.startswith("stub:"):
        return None
    member_id = token.split(":", 1)[1]
    return member_id or None


def member_id_from_request():
    """Resolve the current member id from the Authorization bearer token."""
    from flask import request

    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    token = header[len("Bearer "):].strip()
    return parse_token(token) if token else None


def request_otp(data):
    phone = (data or {}).get("phone")
    if not phone:
        raise BadRequest("phone is required")

    otp = f"{random.randint(0, 999999):06d}"
    ttl = current_app.config["OTP_TTL_SECONDS"]
    _send_telegram_otp(phone, otp, ttl)
    get_redis().setex(_otp_key(phone), ttl, otp)
    response = {"message": "OTP sent"}
    if current_app.debug:
        response["otp_debug"] = otp
    return response


def _send_telegram_otp(phone: str, code: str, ttl: int) -> None:
    """Deliver an OTP via Telegram Gateway. No-op when not configured (dev mode)."""
    token = current_app.config.get("TELEGRAM_GATEWAY_TOKEN")
    if not token:
        current_app.logger.info("Telegram Gateway not configured; skipping delivery")
        return

    body = {
        "phone_number": phone,
        "code": code,
        "ttl": ttl,
    }
    sender = current_app.config.get("TELEGRAM_GATEWAY_SENDER_USERNAME")
    if sender:
        body["sender_username"] = sender

    req = urllib.request.Request(
        TELEGRAM_GATEWAY_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    generic_error = "Could not send verification code. Please try again later."
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="ignore")
        current_app.logger.error("Telegram Gateway HTTP %s: %s", e.code, detail)
        raise BadRequest(generic_error)
    except urllib.error.URLError as e:
        current_app.logger.error("Telegram Gateway unreachable: %s", e.reason)
        raise BadRequest(generic_error)

    if not payload.get("ok"):
        current_app.logger.error("Telegram Gateway rejected: %s", payload.get("error"))
        raise BadRequest(generic_error)


def verify_otp(data):
    data = data or {}
    phone = data.get("phone")
    otp = data.get("otp")
    if not phone or not otp:
        raise BadRequest("phone and otp are required")

    r = get_redis()
    key = _otp_key(phone)
    stored = r.get(key)
    if stored is None:
        raise Unauthorized("otp expired or not requested")
    if stored != otp:
        raise Unauthorized("invalid otp")

    r.delete(key)

    existing = member.find_by_phone(phone)
    if existing is None:
        created = member.create({"phone": phone, "signin_type": "phone"})
        return {
            "message": "verified",
            "token": _issue_token(created["id"]),
            "member": created,
            "is_new": True,
        }

    serialized = member.serialize(existing)
    return {
        "message": "verified",
        "token": _issue_token(serialized["id"]),
        "member": serialized,
        "is_new": False,
    }


def google_signin(data):
    """Verify a Google credential and find-or-create a member.

    Accepts either:
      - {"id_token": "..."} from Google Identity Services credential callback
      - {"access_token": "..."} from initTokenClient (custom button flow)
    """
    data = data or {}
    id_tok = data.get("id_token")
    access_tok = data.get("access_token")
    if not id_tok and not access_tok:
        raise BadRequest("id_token or access_token is required")

    client_id = current_app.config.get("GOOGLE_CLIENT_ID")
    if not client_id:
        raise BadRequest("Google sign-in is not configured")

    info = _resolve_google_user(id_tok, access_tok, client_id)

    google_id = info.get("sub")
    if not google_id:
        raise Unauthorized("Google response missing subject")

    existing = member.find_by_google_id(google_id)
    if existing is None and info.get("email"):
        existing = member.find_by_email(info["email"])

    if existing is None:
        created = member.create({
            "google_id": google_id,
            "email": info.get("email"),
            "name": info.get("name"),
            "avatar_url": info.get("picture"),
            "signin_type": "google",
        })
        return {
            "message": "verified",
            "token": _issue_token(created["id"]),
            "member": created,
        }

    serialized = member.serialize(existing)
    return {
        "message": "verified",
        "token": _issue_token(serialized["id"]),
        "member": serialized,
    }


def _resolve_google_user(id_tok, access_tok, client_id):
    if id_tok:
        try:
            from google.oauth2 import id_token as google_id_token
            from google.auth.transport import requests as google_requests
            return google_id_token.verify_oauth2_token(
                id_tok, google_requests.Request(), client_id
            )
        except ValueError as e:
            raise Unauthorized(f"invalid Google token: {e}")

    # access_token: hit Google's userinfo endpoint (no library dep beyond stdlib)
    import json
    import urllib.error
    import urllib.request
    req = urllib.request.Request(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_tok}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise Unauthorized(f"invalid Google access_token: {e.code}")
    except urllib.error.URLError as e:
        raise Unauthorized(f"could not reach Google: {e.reason}")


def telegram_signin(data):
    """Verify a Telegram Login Widget payload and find-or-create a member.

    HMAC_SHA256 of the data_check_string, keyed by SHA256(bot_token).
    https://core.telegram.org/widgets/login#checking-authorization
    """
    payload = dict(data or {})
    received_hash = payload.pop("hash", None)
    if not received_hash:
        raise BadRequest("hash is required")
    if "id" not in payload:
        raise BadRequest("id is required")

    bot_token = current_app.config.get("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise BadRequest("Telegram sign-in is not configured")

    data_check_string = "\n".join(
        f"{k}={payload[k]}" for k in sorted(payload.keys()) if payload[k] is not None
    )
    secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()
    expected = hmac.new(
        secret_key, data_check_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, received_hash):
        raise Unauthorized("invalid Telegram signature")

    auth_date = int(payload.get("auth_date", 0))
    max_age = current_app.config["TELEGRAM_AUTH_MAX_AGE"]
    if auth_date and (time.time() - auth_date) > max_age:
        raise Unauthorized("Telegram auth expired")

    telegram_id = str(payload["id"])
    existing = member.find_by_telegram_id(telegram_id)

    if existing is None:
        name_parts = [payload.get("first_name"), payload.get("last_name")]
        name = " ".join(p for p in name_parts if p) or payload.get("username")
        created = member.create({
            "telegram_id": telegram_id,
            "name": name,
            "avatar_url": payload.get("photo_url"),
            "signin_type": "telegram",
        })
        return {
            "message": "verified",
            "token": _issue_token(created["id"]),
            "member": created,
        }

    serialized = member.serialize(existing)
    return {
        "message": "verified",
        "token": _issue_token(serialized["id"]),
        "member": serialized,
    }
