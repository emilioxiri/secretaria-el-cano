"""
Makefile for common development tasks.
"""

.PHONY: help install run test clean lint format

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies with Poetry
	poetry install

install-dev: ## Install development dependencies
	poetry install --with dev

run: ## Run the Streamlit application
	poetry run streamlit run app.py

test: ## Run tests
	poetry run python -m pytest tests/ -v

test-coverage: ## Run tests with coverage
	poetry run python -m pytest tests/ --cov=. --cov-report=html

lint: ## Run linting with flake8
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

format: ## Format code with black
	poetry run black .

clean: ## Clean cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

setup-db: ## Set up database (run MySQL container)
	./run_mysql_container.sh

docker-build: ## Build Docker image
	docker build -t secretaria-el-cano .

docker-run: ## Run application in Docker
	docker run -p 8501:8501 secretaria-el-cano