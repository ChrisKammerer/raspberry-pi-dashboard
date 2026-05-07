.PHONY: install build run clean help

# Install Python package in development mode
install:
	uv pip install -e .

# Build Docker image
build:
	docker compose build

# Run the weather-fetch command in Docker
run:
	docker compose run --rm dashboard weather-fetch

start:
	docker compose up -d

EXEC_CMD ?= bash
exec:
	docker compose exec -T dashboard $(EXEC_CMD)

stop: 
	docker compose down

# Clean up Docker resources
clean:
	docker compose down --volumes --remove-orphans
	docker system prune -f

# Show available commands
help:
	@echo "Available commands:"
	@echo "  install   - Install Python package with uv"
	@echo "  build     - Build Docker image"
	@echo "  run       - Run weather-fetch in Docker"
	@echo "  start     - Start services in detached mode"
	@echo "  exec      - Exec into dashboard container; use EXEC_CMD=... to run a specific command"
	@echo "  stop      - Stop Docker Compose"
	@echo "  clean     - Clean up Docker resources"
	@echo "  help      - Show this help message"