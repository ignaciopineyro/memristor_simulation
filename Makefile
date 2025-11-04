.PHONY: help build up down restart logs shell test clean

COMPOSE_FILE = docker-compose.yml
SERVICE_NAME = web

help:
	@echo "Available commands:"
	@echo "  build     - Build the Docker image"
	@echo "  up        - Start the application"
	@echo "  down      - Stop the application"
	@echo "  restart   - Restart the application"
	@echo "  logs      - View real-time logs"
	@echo "  shell     - Access the container shell"
	@echo "  test      - Run tests"
	@echo "  clean     - Clean up containers and volumes"

build:
	docker-compose build

up:
	docker-compose up
	@echo "App available at http://localhost:8000"

up-build:
	docker-compose up --build
	@echo "App built and available at http://localhost:8000"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

shell:
	docker-compose exec $(SERVICE_NAME) bash

test:
	docker-compose exec $(SERVICE_NAME) python -m pytest

migrate:
	docker-compose exec $(SERVICE_NAME) python manage.py migrate

collectstatic:
	docker-compose exec $(SERVICE_NAME) python manage.py collectstatic --noinput

clean:
	docker-compose down -v
	docker system prune -f

clean-all:
	docker-compose down -v
	docker system prune -af

status:
	docker-compose ps

dev-up:
	docker-compose -f docker-compose.yml up

dev-logs:
	docker-compose logs -f $(SERVICE_NAME)

backup:
	docker run --rm -v memristor_simulation_simulation_results:/backup-vol -v $(PWD):/backup alpine tar czf /backup/simulation_results_backup.tar.gz -C /backup-vol .
	@echo "Backup created: simulation_results_backup.tar.gz"