.PHONY: dev api web build install stop clean help

help:
	@echo "Targets:"
	@echo "  make dev      Run API (Docker) + webpage (Nuxt) together with live logs"
	@echo "  make api      Run only the Flask API + ArangoDB + Redis via docker compose"
	@echo "  make web      Run only the Nuxt dev server"
	@echo "  make build    Rebuild the API image (run after changing requirements.txt or Dockerfile)"
	@echo "  make install  Install webpage dependencies (bun)"
	@echo "  make stop     Stop API containers"
	@echo "  make clean    Stop API containers and wipe ArangoDB + Redis volumes"

dev:
	@if [ ! -f api/.env ]; then cp api/.env.example api/.env; echo "Created api/.env from .env.example"; fi
	@if [ ! -d webpage/node_modules ]; then $(MAKE) install; fi
	@echo "Starting API on http://localhost:5001 and webpage on http://localhost:3000 (both with hot reload)"
	@trap 'echo; echo "Stopping..."; kill 0' INT TERM; \
		( cd api && docker compose up ) & \
		( cd webpage && bun run dev ) & \
		wait

api:
	@if [ ! -f api/.env ]; then cp api/.env.example api/.env; fi
	cd api && docker compose up

build:
	cd api && docker compose build

web:
	@if [ ! -d webpage/node_modules ]; then $(MAKE) install; fi
	cd webpage && bun run dev

install:
	cd webpage && bun install

stop:
	cd api && docker compose down

clean:
	cd api && docker compose down -v
