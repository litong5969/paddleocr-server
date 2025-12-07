SHELL := /bin/bash

.PHONY: test selfcheck perf-baseline

test:
	./scripts/dev/run_tests.sh

selfcheck:
	./scripts/dev/selfcheck.sh

perf-baseline:
	./scripts/dev/perf_baseline.sh
