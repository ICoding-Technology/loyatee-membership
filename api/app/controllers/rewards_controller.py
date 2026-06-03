from app.controllers.errors import BadRequest, NotFound
from app.models import reward, store


def list_store_rewards(store_id, active_only=True):
    if not store.find_by_id(store_id):
        raise NotFound("store not found")
    return reward.list_for_store(store_id, active_only=active_only)


def create_reward(store_id, data):
    data = data or {}
    if not store.find_by_id(store_id):
        raise NotFound("store not found")
    if not data.get("name"):
        raise BadRequest("name is required")
    cost = data.get("points_cost")
    if not isinstance(cost, int) or cost < 0:
        raise BadRequest("points_cost must be a non-negative integer")
    return reward.create(store_id, data)


def get_reward(reward_id):
    doc = reward.find_by_id(reward_id)
    if not doc:
        raise NotFound("reward not found")
    return reward.serialize(doc)


def update_reward(reward_id, data):
    updated = reward.update(reward_id, data or {})
    if not updated:
        raise NotFound("reward not found")
    return updated


def delete_reward(reward_id):
    if not reward.delete(reward_id):
        raise NotFound("reward not found")
    return {"message": "deleted"}
