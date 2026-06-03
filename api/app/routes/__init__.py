from app.routes.health import health_bp
from app.routes.auth import auth_bp
from app.routes.members import members_bp
from app.routes.profile import profile_bp
from app.routes.stores import stores_bp
from app.routes.memberships import memberships_bp
from app.routes.subscribe import subscribe_bp
from app.routes.rewards import rewards_bp


def register_blueprints(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(members_bp, url_prefix="/api/members")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(stores_bp, url_prefix="/api/stores")
    app.register_blueprint(memberships_bp, url_prefix="/api/memberships")
    app.register_blueprint(subscribe_bp, url_prefix="/api/subscribe")
    app.register_blueprint(rewards_bp, url_prefix="/api/rewards")
