.PHONY: help test test-verbose test-coverage coverage-report clean deps test-run check

help:
	@echo "Available targets:"
	@echo "  make test              - Run all tests"
	@echo "  make test-verbose      - Run tests with verbose output"
	@echo "  make test-coverage     - Run tests with coverage report"
	@echo "  make coverage-report   - Generate HTML coverage report"
	@echo "  make clean             - Clean test artifacts"
	@echo "  make deps              - Install development dependencies"
	@echo "  make test-run          - Run tests matching a pattern"
	@echo "  make check             - Run the default validation checks"

test:
	python -m pytest

test-verbose:
	python -m pytest -vv

test-coverage:
	python -m pytest --cov=gh_sync_labels --cov-report=term-missing

coverage-report:
	python -m pytest --cov=gh_sync_labels --cov-report=html
	@echo "Coverage report generated: htmlcov/index.html"

clean:
	rm -rf .pytest_cache .coverage htmlcov

deps:
	python -m pip install -r requirements-dev.txt

test-run:
	@read -p "Enter pytest pattern: " test; \
	python -m pytest -v -k "$$test"

check: test
	@echo "All checks passed!"
