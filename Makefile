.DEFAULT_GOAL := help

export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up migrations	# Stop, build and deploy all services

build:	# Assembling images
	docker compose build

up:		# Deploying all services and creating docker images
	docker compose up -d

down:	# Stop all services and remove containers
	docker compose down --remove-orphans

migrations:		# Create a new revision migration and run migration
	docker-compose run --rm app flask db init
	docker-compose run --rm app flask db migrate
	docker-compose run --rm app flask db upgrade
	docker-compose run --rm app python create_test_users.py

help:	# Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?# .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; {printf "  %-20s %s\n", $$1, $$2}'