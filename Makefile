# Structured Output Cookbook - Makefile
# Provides convenient commands for development and usage

.PHONY: help install dev test lint format clean docker-build docker-run docker-dev

# Default target
help: ## Show this help message
	@echo "🧑‍🍳 Structured Output Cookbook - Available Commands"
	@echo "================================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development Setup
install: ## Install dependencies with uv
	@echo "📦 Installing dependencies..."
	uv sync

dev: install ## Install development dependencies
	@echo "🛠️  Installing development dependencies..."
	uv sync --all-extras

# Code Quality
test: ## Run tests
	@echo "🧪 Running tests..."
	uv run pytest

test-cov: ## Run tests with coverage
	@echo "📊 Running tests with coverage..."
	uv run pytest --cov=src/structured_output_cookbook --cov-report=html

lint: ## Run linting
	@echo "🔍 Running linters..."
	uv run ruff check .
	uv run mypy src/

lint-fix: ## Fix linting issues
	@echo "🔧 Fixing linting issues..."
	uv run ruff --fix .
	uv run black .

format: ## Format code
	@echo "💄 Formatting code..."
	uv run black .
	uv run ruff --fix .

# CLI Commands
list-templates: ## List available predefined templates
	@echo "📋 Available templates:"
	uv run structured-output list-templates

list-schemas: ## List available custom schemas
	@echo "📋 Available schemas:"
	uv run structured-output list-schemas

example-recipe: ## Run recipe extraction example
	@echo "🍝 Running recipe extraction example..."
	uv run structured-output extract recipe --input-file examples/recipe.txt --pretty

example-job: ## Run job description extraction example
	@echo "💼 Running job description extraction example..."
	uv run structured-output extract job --input-file examples/job_description.txt --pretty

example-news: ## Run news article extraction example
	@echo "📰 Running news article extraction example..."
	uv run structured-output extract-custom news_article --input-file examples/news_article.txt --pretty

example-email: ## Run email extraction example
	@echo "📧 Running email extraction example..."
	uv run structured-output extract email --text "Subject: Meeting Tomorrow\nFrom: john@company.com\nHi team, we have an important meeting tomorrow at 2 PM in conference room A. Please bring your reports." --pretty

example-event: ## Run event extraction example
	@echo "🎉 Running event extraction example..."
	uv run structured-output extract event --text "Annual Tech Conference 2024 - Join us on March 15th at San Francisco Convention Center from 9 AM to 6 PM. Registration required." --pretty

example-product-review: ## Run product review extraction example
	@echo "⭐ Running product review extraction example..."
	uv run structured-output extract product-review --text "Amazing laptop! The new MacBook Pro is incredible. 5 stars. Great performance, excellent display. Worth every penny. Highly recommended for developers." --pretty

# Docker Commands
docker-build: ## Build Docker image
	@echo "🐳 Building Docker image..."
	docker build -t structured-output-cookbook:latest .

docker-run: ## Run with Docker (requires OPENAI_API_KEY env var)
	@echo "🐳 Running with Docker..."
	./scripts/docker-run.sh

docker-dev: ## Start development environment with Docker
	@echo "🛠️  Starting Docker development environment..."
	./scripts/docker-dev.sh

docker-compose-up: ## Start services with docker-compose
	@echo "🐳 Starting with docker-compose..."
	docker-compose up --build

docker-compose-run: ## Run command with docker-compose
	@echo "🐳 Running command with docker-compose..."
	docker-compose run --rm structured-output-cookbook $(ARGS)

# Examples with Docker
docker-example-recipe: ## Run recipe extraction example with Docker
	@echo "🍝 Running recipe extraction example with Docker..."
	./scripts/docker-run.sh extract recipe --input-file examples/recipe.txt --pretty

docker-example-job: ## Run job description extraction example with Docker
	@echo "💼 Running job description extraction example with Docker..."
	./scripts/docker-run.sh extract job --input-file examples/job_description.txt --pretty

docker-list-templates: ## List templates with Docker
	@echo "📋 Listing templates with Docker..."
	./scripts/docker-run.sh list-templates

# New CLI Commands
validate-schemas: ## Validate all custom YAML schemas
	@echo "🔍 Validating schemas..."
	uv run structured-output validate-schemas

session-stats: ## Show session statistics
	@echo "📊 Showing session statistics..."
	uv run structured-output session-stats

cost-analysis: ## Show cost analysis and recommendations
	@echo "💰 Showing cost analysis..."
	uv run structured-output cost-analysis

# Batch processing examples
batch-example: ## Run batch extraction example
	@echo "🔄 Running batch extraction example..."
	mkdir -p examples/batch_input examples/batch_output
	echo "Sample recipe 1: Pasta with tomato sauce" > examples/batch_input/recipe1.txt
	echo "Sample recipe 2: Chicken curry with rice" > examples/batch_input/recipe2.txt
	uv run structured-output batch-extract examples/batch_input/*.txt recipe --output-dir examples/batch_output

# Cleanup
clean: ## Clean up build artifacts and cache
	@echo "🧹 Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-docker: ## Clean up Docker images and containers
	@echo "🐳 Cleaning up Docker..."
	docker system prune -f
	docker image prune -f

# Environment Setup
env-example: ## Create example environment file
	@echo "📝 Creating example environment file..."
	@echo "# OpenAI Configuration (Required)" > .env.example
	@echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env.example
	@echo "" >> .env.example
	@echo "# Optional Configuration" >> .env.example
	@echo "OPENAI_MODEL=gpt-4o-mini" >> .env.example
	@echo "LOG_LEVEL=INFO" >> .env.example
	@echo "MAX_TOKENS=4000" >> .env.example
	@echo "TEMPERATURE=0.1" >> .env.example
	@echo "✅ Created .env.example file"

check-env: ## Check if required environment variables are set
	@echo "🔍 Checking environment variables..."
	@if [ -z "$$OPENAI_API_KEY" ]; then \
		echo "❌ OPENAI_API_KEY is not set"; \
		echo "Please set your OpenAI API key:"; \
		echo "export OPENAI_API_KEY='your-api-key-here'"; \
		exit 1; \
	else \
		echo "✅ OPENAI_API_KEY is set"; \
	fi

# Release
build: ## Build the package
	@echo "📦 Building package..."
	uv build

publish: build ## Publish to PyPI (requires authentication)
	@echo "🚀 Publishing to PyPI..."
	uv publish

# Quick Start
quick-start: install check-env example-recipe ## Quick start: install, check env, and run example
	@echo "🎉 Quick start completed successfully!"
	@echo "Try running: make list-templates"

# Development workflow
dev-setup: dev env-example ## Setup development environment
	@echo "🛠️  Development environment setup complete!"
	@echo "Don't forget to:"
	@echo "1. Copy .env.example to .env and add your OpenAI API key"
	@echo "2. Run 'make check-env' to verify setup"
	@echo "3. Run 'make test' to run tests" 