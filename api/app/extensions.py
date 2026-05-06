import redis
from arango import ArangoClient
from flask import current_app, g


COLLECTIONS = ["members"]

_redis_client: "redis.Redis | None" = None


def init_redis(app):
    global _redis_client
    _redis_client = redis.Redis.from_url(
        app.config["REDIS_URL"], decode_responses=True
    )


def get_redis() -> "redis.Redis":
    if _redis_client is None:
        raise RuntimeError("Redis not initialized — call init_redis(app) first")
    return _redis_client


def get_client():
    return ArangoClient(hosts=current_app.config["ARANGO_URL"])


def get_db():
    if "arango_db" not in g:
        client = get_client()
        g.arango_db = client.db(
            current_app.config["ARANGO_DB"],
            username=current_app.config["ARANGO_USER"],
            password=current_app.config["ARANGO_PASSWORD"],
        )
    return g.arango_db


def init_db(app):
    client = ArangoClient(hosts=app.config["ARANGO_URL"])
    sys_db = client.db(
        "_system",
        username=app.config["ARANGO_USER"],
        password=app.config["ARANGO_PASSWORD"],
    )

    db_name = app.config["ARANGO_DB"]
    if not sys_db.has_database(db_name):
        sys_db.create_database(db_name)

    db = client.db(
        db_name,
        username=app.config["ARANGO_USER"],
        password=app.config["ARANGO_PASSWORD"],
    )
    for name in COLLECTIONS:
        if not db.has_collection(name):
            db.create_collection(name)

    members = db.collection("members")
    _ensure_unique_index(members, ["phone"], sparse=True)
    _ensure_unique_index(members, ["google_id"], sparse=True)
    _ensure_unique_index(members, ["telegram_id"], sparse=True)
    _ensure_unique_index(members, ["account_id"], sparse=True)


def _ensure_unique_index(collection, fields, sparse):
    for idx in collection.indexes():
        if (
            idx.get("fields") == fields
            and idx.get("type") == "hash"
            and idx.get("unique")
        ):
            if idx.get("sparse", False) == sparse:
                return
            collection.delete_index(idx["id"])
            break
    collection.add_hash_index(fields=fields, unique=True, sparse=sparse)
