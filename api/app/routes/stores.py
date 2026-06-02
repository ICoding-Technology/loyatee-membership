from flask import Blueprint, request, jsonify

from app.controllers import stores_controller

stores_bp = Blueprint("stores", __name__)


@stores_bp.get("")
def list_stores():
    return jsonify(stores_controller.list_stores())


@stores_bp.post("")
def create_store():
    return jsonify(stores_controller.create_store(request.get_json())), 201


@stores_bp.get("/by-token")
def resolve_store():
    return jsonify(stores_controller.resolve_store(request.args.get("token")))


@stores_bp.get("/<store_id>")
def get_store(store_id):
    return jsonify(stores_controller.get_store(store_id))


@stores_bp.patch("/<store_id>")
def update_store(store_id):
    return jsonify(stores_controller.update_store(store_id, request.get_json()))


@stores_bp.delete("/<store_id>")
def delete_store(store_id):
    return jsonify(stores_controller.delete_store(store_id))
