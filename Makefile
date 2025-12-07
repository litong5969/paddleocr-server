.PHONY: up down logs selfcheck test perf-baseline

up:
	docker compose --compatibility up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

selfcheck:
	bash scripts/dev/selfcheck.sh

test:
	bash scripts/dev/run_tests.sh

perf-baseline:
	bash scripts/dev/perf_baseline.sh
