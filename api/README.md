# Loyatee API

Flask API for the Loyatee membership app, backed by ArangoDB.

## Run with Docker Compose (recommended)

```bash
cp .env.example .env
docker compose up --build
```

- API → http://localhost:5000
- ArangoDB web UI → http://localhost:8529 (user `root`, password from `.env`)

Rebuild after dependency changes:

```bash
docker compose up --build --force-recreate
```

Tear down (keeps volumes):

```bash
docker compose down
```

Wipe data:

```bash
docker compose down -v
```

## Run locally without Docker

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python wsgi.py
```

Point `ARANGO_URL` at a running ArangoDB (start one with `docker compose up arangodb`).

## Structure

```
api/
├── app/
│   ├── __init__.py         # app factory
│   ├── extensions.py       # arango client + init
│   ├── models/             # document helpers (member)
│   └── routes/             # blueprints (health, auth, members)
├── config.py
├── wsgi.py
└── requirements.txt
```

## Endpoints

- `GET /health`
- `POST /api/auth/request-otp`
- `POST /api/auth/verify-otp`
- `GET|POST /api/members`
- `GET|PATCH|DELETE /api/members/<id>` (id is the Arango `_key`)
