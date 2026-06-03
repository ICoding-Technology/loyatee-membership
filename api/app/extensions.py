import redis
from arango import ArangoClient
from arango.exceptions import CollectionCreateError, IndexCreateError
from flask import current_app, g


DOCUMENT_COLLECTIONS = [
    "members",
    "stores",
    "rewards",
    "transactions",
    "transactions_archive",
]
EDGE_COLLECTIONS = ["memberships"]

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
    db_name = app.config["ARANGO_DB"]
    user = app.config["ARANGO_USER"]
    password = app.config["ARANGO_PASSWORD"]

    # In dev/bootstrap, ARANGO_BOOTSTRAP=1 lets us connect to _system and
    # create the database if missing. In production the DB user usually has
    # no access to _system, so default to skipping that step.
    if app.config.get("ARANGO_BOOTSTRAP"):
        sys_db = client.db("_system", username=user, password=password)
        if not sys_db.has_database(db_name):
            sys_db.create_database(db_name)

    db = client.db(db_name, username=user, password=password)
    for name in DOCUMENT_COLLECTIONS:
        _create_collection(db, name, edge=False)
    for name in EDGE_COLLECTIONS:
        _create_collection(db, name, edge=True)

    members = db.collection("members")
    _ensure_unique_index(members, ["phone"], sparse=True)
    _ensure_unique_index(members, ["google_id"], sparse=True)
    _ensure_unique_index(members, ["telegram_id"], sparse=True)
    _ensure_unique_index(members, ["account_id"], sparse=True)

    stores = db.collection("stores")
    _ensure_unique_index(stores, ["slug"], sparse=True)
    _ensure_unique_index(stores, ["uuid"], sparse=True)
    _ensure_persistent_index(stores, ["status"], unique=False, sparse=False)

    # One subscription per (member, store). The edge index already covers
    # OUTBOUND/INBOUND traversal; this just blocks duplicate subscriptions.
    memberships = db.collection("memberships")
    _ensure_persistent_index(memberships, ["_from", "_to"], unique=True, sparse=False)

    # Hot ledger: balance reads filter by (membership_id, period); the
    # statement view reads by (membership_id, created_at).
    transactions = db.collection("transactions")
    _ensure_persistent_index(
        transactions, ["membership_id", "period"], unique=False, sparse=False
    )
    _ensure_persistent_index(
        transactions, ["membership_id", "created_at"], unique=False, sparse=False
    )
    # Idempotent period close: at most one opening row per (membership, period).
    _ensure_persistent_index(
        transactions, ["membership_id", "period", "type"], unique=False, sparse=False
    )

    archive = db.collection("transactions_archive")
    _ensure_persistent_index(
        archive, ["membership_id", "created_at"], unique=False, sparse=False
    )

    rewards = db.collection("rewards")
    _ensure_persistent_index(rewards, ["store_id"], unique=False, sparse=False)


def _create_collection(db, name, edge):
    try:
        db.create_collection(name, edge=edge)
    except CollectionCreateError as e:
        # 1207 = duplicate name. Another worker raced us — that's fine.
        if e.error_code != 1207:
            raise


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
    try:
        collection.add_hash_index(fields=fields, unique=True, sparse=sparse)
    except IndexCreateError:
        # Another worker raced us. Index already exists — fine.
        pass


def _ensure_persistent_index(collection, fields, unique, sparse):
    for idx in collection.indexes():
        if (
            idx.get("fields") == fields
            and idx.get("type") == "persistent"
            and idx.get("unique", False) == unique
        ):
            return
    try:
        collection.add_persistent_index(fields=fields, unique=unique, sparse=sparse)
    except IndexCreateError:
        # Another worker raced us. Index already exists — fine.
        pass
