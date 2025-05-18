.PHONY: setup install test lint format clean

setup:
	@echo "Setting up development environment..."
	poetry install
	cd frontend && npm install

install:
	@echo "Installing dependencies..."
	poetry install
	cd frontend && npm install

test:
	@echo "Running tests..."
	poetry run pytest backend/tests
	cd frontend && npm test

lint:
	@echo "Running linters..."
	poetry run flake8 backend
	poetry run mypy backend
	cd frontend && npm run lint

format:
	@echo "Formatting code..."
	poetry run black backend
	poetry run isort backend
	cd frontend && npm run format

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name "node_modules" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} + 