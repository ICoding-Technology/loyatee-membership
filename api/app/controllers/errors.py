class AppError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


class NotFound(AppError):
    status_code = 404


class Conflict(AppError):
    status_code = 409


class Unauthorized(AppError):
    status_code = 401


class BadRequest(AppError):
    status_code = 400


def register_error_handlers(app):
    from flask import jsonify

    @app.errorhandler(AppError)
    def handle_app_error(err):
        return jsonify({"error": err.message}), err.status_code
