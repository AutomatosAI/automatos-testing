
# Automotas AI Testing Framework Makefile
# =======================================

.PHONY: help install setup test test-unit test-integration test-e2e test-performance test-security clean docker-up docker-down reports

# Default target
help:
	@echo "🧪 Automotas AI Testing Framework"
	@echo "================================="
	@echo ""
	@echo "Available targets:"
	@echo "  install          Install dependencies"
	@echo "  setup            Set up test environment"
	@echo "  test             Run all tests"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-e2e         Run end-to-end tests"
	@echo "  test-performance Run performance tests"
	@echo "  test-security    Run security tests"
	@echo "  docker-up        Start test infrastructure"
	@echo "  docker-down      Stop test infrastructure"
	@echo "  reports          Generate test reports"
	@echo "  clean            Clean up test artifacts"
	@echo ""

# Installation and setup
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

setup: install
	@echo "🔧 Setting up test environment..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "📋 Created .env file from template"; fi
	mkdir -p reports test_data logs
	@echo "✅ Test environment ready"

# Test execution targets
test: setup
	@echo "🧪 Running all tests..."
	python run_tests.py --reports --parallel

test-unit: setup
	@echo "🔬 Running unit tests..."
	python run_tests.py --level unit --reports

test-integration: setup
	@echo "🔗 Running integration tests..."
	python run_tests.py --level integration --reports

test-e2e: setup
	@echo "🎯 Running end-to-end tests..."
	python run_tests.py --level e2e --reports

test-performance: setup
	@echo "⚡ Running performance tests..."
	python run_tests.py --filter performance --reports

test-security: setup
	@echo "🔒 Running security tests..."
	python run_tests.py --filter security --level security --reports

# Specific test suites
test-agents: setup
	@echo "🤖 Testing agent management..."
	python run_tests.py --filter agents --reports

test-workflows: setup
	@echo "🔄 Testing workflow orchestration..."
	python run_tests.py --filter workflows --reports

test-context: setup
	@echo "🧠 Testing context engineering..."
	python run_tests.py --filter context_engineering --reports

test-multi-agent: setup
	@echo "👥 Testing multi-agent systems..."
	python run_tests.py --filter multi_agent --reports

test-memory: setup
	@echo "🧩 Testing memory systems..."
	python run_tests.py --filter memory_systems --reports

# Docker infrastructure
docker-up:
	@echo "🐳 Starting test infrastructure..."
	docker-compose up -d
	@echo "⏳ Waiting for services to be ready..."
	sleep 10
	@echo "✅ Test infrastructure ready"

docker-down:
	@echo "🛑 Stopping test infrastructure..."
	docker-compose down

docker-clean: docker-down
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down -v
	docker system prune -f

# Environment-specific testing
test-dev: setup
	@echo "🔧 Running tests against development environment..."
	python run_tests.py --environment development --reports

test-staging: setup
	@echo "🚀 Running tests against staging environment..."
	python run_tests.py --environment staging --reports

test-prod: setup
	@echo "🏭 Running tests against production environment..."
	python run_tests.py --environment production --reports --filter "not destructive"

# Reporting and analysis
reports:
	@echo "📊 Generating test reports..."
	@if [ -d reports ]; then \
		echo "Latest test reports:"; \
		ls -la reports/ | head -10; \
		echo ""; \
		echo "📈 Open reports/test_report_*.html in your browser"; \
	else \
		echo "No reports found. Run tests first with --reports flag"; \
	fi

view-reports:
	@echo "🌐 Starting report server..."
	@if command -v python3 >/dev/null 2>&1; then \
		cd reports && python3 -m http.server 8080 & \
		echo "📊 Reports available at http://localhost:8080"; \
		echo "Press Ctrl+C to stop the server"; \
	else \
		echo "Python not found. Please open reports/test_report_*.html manually"; \
	fi

# Continuous integration targets
ci-test: docker-up
	@echo "🔄 Running CI tests..."
	python run_tests.py --reports --parallel --environment development
	$(MAKE) docker-down

ci-security-scan:
	@echo "🛡️ Running security scans for CI..."
	python run_tests.py --filter security --level security --reports --environment staging

# Development helpers
format:
	@echo "💅 Formatting code..."
	black framework/ tests/ --line-length 100
	isort framework/ tests/ --profile black

lint:
	@echo "🔍 Linting code..."
	flake8 framework/ tests/ --max-line-length 100 --ignore E203,W503
	mypy framework/ tests/ --ignore-missing-imports

validate: format lint
	@echo "✅ Code validation complete"

# Monitoring and maintenance
health-check:
	@echo "🏥 Checking system health..."
	@if curl -s http://localhost:8002/health >/dev/null 2>&1; then \
		echo "✅ Automotas AI backend is healthy"; \
	else \
		echo "❌ Automotas AI backend is not responding"; \
	fi
	@if curl -s http://localhost:5678 >/dev/null 2>&1; then \
		echo "✅ N8N is running"; \
	else \
		echo "⚠️ N8N is not running (optional)"; \
	fi

logs:
	@echo "📜 Recent test logs..."
	@if [ -d logs ]; then \
		tail -50 logs/test_runner.log 2>/dev/null || echo "No test logs found"; \
	else \
		echo "No logs directory found"; \
	fi

# Cleanup
clean:
	@echo "🧹 Cleaning up test artifacts..."
	rm -rf __pycache__ .pytest_cache .coverage
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name ".DS_Store" -delete
	@echo "✅ Cleanup complete"

clean-reports:
	@echo "🗑️ Cleaning up old reports..."
	@if [ -d reports ]; then \
		find reports/ -name "*.html" -mtime +7 -delete; \
		find reports/ -name "*.json" -mtime +7 -delete; \
		find reports/ -name "*.xml" -mtime +7 -delete; \
		echo "✅ Old reports cleaned up"; \
	fi

clean-all: clean clean-reports docker-clean
	@echo "🧹 Full cleanup complete"

# Help for specific components
help-docker:
	@echo "🐳 Docker Commands:"
	@echo "  make docker-up     - Start PostgreSQL, Redis, and N8N containers"
	@echo "  make docker-down   - Stop all containers"
	@echo "  make docker-clean  - Remove all containers and volumes"

help-testing:
	@echo "🧪 Testing Commands:"
	@echo "  make test          - Run all tests with reports"
	@echo "  make test-agents   - Test agent management only"
	@echo "  make test-workflows - Test workflow orchestration only"
	@echo "  make test-security - Run security tests only"
	@echo "  make ci-test      - Run CI/CD pipeline tests"

# Version info
version:
	@echo "🧪 Automotas AI Testing Framework"
	@python -c "from framework import __version__; print(f'Version: {__version__}')"
	@python --version
	@echo "Dependencies:"
	@pip list | grep -E "(pytest|aiohttp|requests)"
