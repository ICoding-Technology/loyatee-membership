import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    ARANGO_URL = os.getenv("ARANGO_URL", "http://localhost:8529")
    ARANGO_DB = os.getenv("ARANGO_DB", "loyatee")
    ARANGO_USER = os.getenv("ARANGO_USER", "root")
    ARANGO_PASSWORD = os.getenv("ARANGO_PASSWORD", "")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
