from app.routes.health import health_bp
from app.routes.auth import auth_bp
from app.routes.members import members_bp


def register_blueprints(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(members_bp, url_prefix="/api/members")
