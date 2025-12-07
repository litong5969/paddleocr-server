.PHONY: up down logs selfcheck

up:
	docker compose --compatibility up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

selfcheck:
	bash scripts/dev/selfcheck.sh

