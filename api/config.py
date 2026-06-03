import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    ARANGO_URL = os.getenv("ARANGO_URL", "http://localhost:8529")
    ARANGO_DB = os.getenv("ARANGO_DB", "loyatee")
    ARANGO_USER = os.getenv("ARANGO_USER", "root")
    ARANGO_PASSWORD = os.getenv("ARANGO_PASSWORD", "")
    ARANGO_BOOTSTRAP = os.getenv("ARANGO_BOOTSTRAP", "0") == "1"

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    OTP_TTL_SECONDS = int(os.getenv("OTP_TTL_SECONDS", "300"))

    # Access JWTs are signed with SECRET_KEY (HS256), short-lived (1h). Clients
    # silently swap an expired access token for a new one using the refresh
    # token (opaque, stored in Redis), which lives REFRESH_TTL_SECONDS (30d).
    JWT_ALGORITHM = "HS256"
    JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS", "3600"))
    REFRESH_TTL_SECONDS = int(os.getenv("REFRESH_TTL_SECONDS", str(30 * 24 * 3600)))

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_AUTH_MAX_AGE = int(os.getenv("TELEGRAM_AUTH_MAX_AGE", "86400"))
    TELEGRAM_GATEWAY_TOKEN = os.getenv("TELEGRAM_GATEWAY_TOKEN", "")
    TELEGRAM_GATEWAY_SENDER_USERNAME = os.getenv("TELEGRAM_GATEWAY_SENDER_USERNAME", "")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
