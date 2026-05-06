# syntax=docker/dockerfile:1.7

# Build context: repo root.

# ---- Stage 1: build the Nuxt SPA with Bun ----
FROM oven/bun:1 AS webapp-builder
WORKDIR /webapp

COPY webpage/package.json webpage/bun.lock ./
RUN bun install --frozen-lockfile

COPY webpage/ ./
RUN bun run generate

# ---- Stage 2: Python + Flask, bundling the built SPA ----
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STATIC_DIR=/app/static

WORKDIR /app

COPY api/requirements.txt .
RUN pip install -r requirements.txt

COPY api/ .
COPY --from=webapp-builder /webapp/.output/public /app/static

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "wsgi:app"]
