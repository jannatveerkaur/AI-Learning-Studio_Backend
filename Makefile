.PHONY: help install install-dev run test clean format lint

help:
	@echo "Smart Video Learning Tool - Available Commands:"
	@echo ""
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install all dependencies (including dev)"
	@echo "  make run          - Start the FastAPI server"
	@echo "  make test         - Run all tests"
	@echo "  make test-cov     - Run tests with coverage report"
	@echo "  make clean        - Remove cache and temporary files"
	@echo "  make format       - Format code with black"
	@echo "  make lint         - Lint code with flake8"
	@echo ""

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

run:
	uvicorn main:app --reload

test:
	pytest -v

test-cov:
	pytest --cov=services --cov=. --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

format:
	black main.py config.py models.py services/ tests/ example_client.py

lint:
	flake8 main.py config.py models.py services/ tests/ example_client.py
