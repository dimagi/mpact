start: ## Start the docker containers
	@echo "Starting the docker containers"
	@docker-compose up -d
	@echo "Containers started - http://localhost:8000"

stop: ## Stop Containers
	@docker-compose down

build: ## Build Containers
	@docker-compose build

ssh: ## SSH into running web container
	docker-compose exec web bash

migrations: ## Create DB migrations in the container
	@docker-compose exec web python manage.py makemigrations

migrate: ## Run DB migrations in the container
	@docker-compose exec web python manage.py migrate

shell: ## Get a Django shell
	@docker-compose exec web python manage.py shell

superuser: ## Get a Django shell
	@docker-compose exec web python manage.py createsuperuser

test: ## Run Django tests
	@docker-compose exec web python manage.py test

init: start migrate superuser  ## Quickly get up and running (start containers, migrate DB, create superuser)

npm-install: ## Runs npm install in the container
	@docker-compose exec web npm install

npm-dev: ## Runs npm build in the container (for front-end assets)
	@docker-compose exec web npm run dev

restart:  ## Restart running processes
	@docker-compose restart web celery celerybeat telegram_bot

.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
