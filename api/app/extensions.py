from arango import ArangoClient
from flask import current_app, g


COLLECTIONS = ["members"]


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
    members.add_hash_index(fields=["phone"], unique=True, sparse=False)
