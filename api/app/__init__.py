import json
import os
from flask import Flask, Response, send_from_directory
from flask_cors import CORS

from config import config
from app.extensions import init_db, init_redis
from app.routes import register_blueprints
from app.controllers.errors import register_error_handlers


def create_app(config_name=None):
    static_dir = os.getenv("STATIC_DIR")
    app = Flask(
        __name__,
        static_folder=static_dir,
        static_url_path="/static-assets" if static_dir else None,
    )
    config_name = config_name or os.getenv("FLASK_ENV", "default")
    app.config.from_object(config[config_name])

    CORS(app)
    init_db(app)
    init_redis(app)

    register_blueprints(app)
    register_error_handlers(app)
    _register_runtime_config(app)

    if static_dir:
        _register_spa(app, static_dir)

    return app


def _register_runtime_config(app):
    """Serve /config.js so the SPA can read public config injected at runtime
    (compose env vars), instead of values baked at build time."""

    @app.route("/config.js")
    def runtime_config():
        payload = {
            # Empty string = same-origin relative URLs. Override only if the
            # API is served on a different origin than the SPA.
            "apiBase": os.getenv("PUBLIC_API_BASE", ""),
            "googleClientId": os.getenv("GOOGLE_CLIENT_ID", ""),
            "telegramBotName": os.getenv("TELEGRAM_BOT_NAME", ""),
        }
        body = f"window.__APP_CONFIG__={json.dumps(payload)};"
        resp = Response(body, mimetype="application/javascript")
        resp.headers["Cache-Control"] = "no-store"
        return resp


def _register_spa(app, static_dir):
    """Serve the Nuxt SPA. API blueprints register first, so their concrete
    routes win over the catch-all here."""

    @app.route("/")
    def _spa_root():
        return send_from_directory(static_dir, "index.html")

    @app.route("/<path:path>")
    def _spa_catchall(path):
        full = os.path.join(static_dir, path)
        if os.path.isfile(full):
            return send_from_directory(static_dir, path)
        return send_from_directory(static_dir, "index.html")
