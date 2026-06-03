from flask import Blueprint, request, jsonify

from app.controllers import rewards_controller

rewards_bp = Blueprint("rewards", __name__)


@rewards_bp.get("/<reward_id>")
def get_reward(reward_id):
    return jsonify(rewards_controller.get_reward(reward_id))


@rewards_bp.patch("/<reward_id>")
def update_reward(reward_id):
    return jsonify(rewards_controller.update_reward(reward_id, request.get_json()))


@rewards_bp.delete("/<reward_id>")
def delete_reward(reward_id):
    return jsonify(rewards_controller.delete_reward(reward_id))
