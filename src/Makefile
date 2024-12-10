# Variables
DATA_DIR = data
DB_DIR = ${DATA_DIR}/db
LOG_DIR = ${DATA_DIR}/log
STATIC_DIR = ${DATA_DIR}/static/media

DEPLOY ?= false

# Macros
DOCKER_COMPOSE = docker compose
DOCKER_COMPOSE_DP = docker-compose
DC_RUN_APP = run --rm ft_form sh -c
DC_RUN_DB = run --rm db_form sh -c
DEPLOY_COMPOSE_FILE = -f docker-compose-deploy.yml

all: build

# Target to create directories
create-dirs:
	@echo "Creating directories..." 
	@mkdir -p $(DB_DIR) $(LOG_DIR) $(STATIC_DIR)

# Target to download official Docker images
pull-images:
	@echo "Pulling official Docker images..."
	@docker pull python:3.12.4-alpine3.19
	@docker pull postgres:13-alpine
ifeq ($(DEPLOY), false)
	@docker pull adminer
endif

# DEBUG

build: create-dirs pull-images
	@echo "Building Docker images..."
	@$(DOCKER_COMPOSE) build
#	@chmod -R 777 data/log/
	@$(DOCKER_COMPOSE) $(DC_RUN_APP) "python manage.py wait_for_db"
	@rm -rf app/core/migrations/__pycache__/*
	@if [ -f "app/core/migrations/0001_initial.py" ]; then \
        rm "app/core/migrations/0001_initial.py"; \
    fi

up:
	@echo "Running setup tasks..."
# @$(DOCKER_COMPOSE) $(DC_RUN_APP) "python manage.py test"
	@$(DOCKER_COMPOSE) up

super:
	@echo "Creating superuser..."
	@$(DOCKER_COMPOSE) $(DC_RUN_APP) "python manage.py createsuperuser"

status: 
	@echo "Control status app..."
	@$(DOCKER_COMPOSE) ps

control:
	@echo "Control flake8.."
	@$(DOCKER_COMPOSE) $(DC_RUN_APP) "flake8"

mi:
	@echo "Running Migrations..."
# @chmod -R 777  app/core/migrations/
	@$(DOCKER_COMPOSE) $(DC_RUN_APP) "python manage.py makemigrations"
	@$(DOCKER_COMPOSE) $(DC_RUN_APP) "python manage.py migrate"
	
down:
	@echo "Turning off everything."
	@$(DOCKER_COMPOSE) down

clean: down
	@echo "Cleaning up data directories..."
	@$(DOCKER_COMPOSE) $(DC_RUN_DB) "rm -rf var/lib/postgresql/data/*"
#	@$(DOCKER_COMPOSE) $(DC_RUN_APP) "rm -rf /vol/log/*"
	@echo "Data and log directories cleaned."

fclean: clean
	@echo "Deleting all Docker resources..."
	@docker image rm src-ft_form
	@docker volume rm src_db-data src_static-data src_media-data
	@docker-compose down --rmi all --volumes --remove-orphans
	@docker system prune -a --volumes
	@rm -rf app/core/migrations/__pycache__/*
	@if [ -f "app/core/migrations/0001_initial.py" ]; then \
        rm "app/core/migrations/0001_initial.py"; \
    fi
	@echo "Deleted containers, images, and volumes."
	@rm -rf $(DB_DIR)  $(LOG_DIR)
	
re: fclean all

toma: 
	@find . -name '*.pyc' -delete
# find . -type d -name ".pytest_cache" -exec rm -rf {} +

# DEPLOY
deploy: deploy-build

deploy-build: create-dirs pull-images
	@echo "Building Docker images..."
	@$(DOCKER_COMPOSE_DP) $(DEPLOY_COMPOSE_FILE) build --no-cache

deploy-up:
	@echo "Running setup tasks..."
	@$(DOCKER_COMPOSE_DP) $(DC_RUN_APP) "python manage.py test"
	@$(DOCKER_COMPOSE_DP) $(DEPLOY_COMPOSE_FILE) up --remove-orphans

deploy-down:
	@echo "Turning off everything."
	@$(DOCKER_COMPOSE_DP) $(DEPLOY_COMPOSE_FILE) down

deploy-clean: deploy-down
	@echo "Cleaning up data directories..."
	#@$(DOCKER_COMPOSE_DP) $(DC_RUN_DB) $(DEPLOY_COMPOSE_FILE) "rm -rf /var/lib/postgresql/data/*"

deploy-fclean: deploy-clean

	@echo "Delete All..."
	@docker images --format "{{.Repository}}:{{.Tag}}" | grep "^src" | xargs -r docker rmi
	@docker volume ls --format "{{.Name}}" | grep "^src" | xargs -r docker volume rm
	@docker volume prune -f

.PHONY: all create-dirs pull-images build up clean down fclean super status \
test control mi deploy-build deploy-up deploy-mi deploy-down deploy-mi

# Idiomas
# 	docker compose run --rm app sh -c "python manage.py update_online_status"

# 	docker compose run --rm app sh -c "python manage.py makemessages -l <IDIOMA>"
# 	docker compose run --rm app sh -c "python manage.py compilemessages"

# make deploy-up DEPLOY=true
# export DEPLOY=true en el servidor

# Linux HOST
# export DOCKER_COMPOSE_PATH="$HOME/ft_transcendence/src/docker-compose-deploy.yml"
# sudo yum install cronie
# sudo systemctl start cron
# sudo systemctl enable cron

# */15 * * * * /path/to/your/venv/bin/python /path/to/your/manage.py update_online_status
# */1 * * * * $HOME/ft_transcendence/toma.sh >> $HOME/update_online_status.log 2>&1

# crontab -l

# delete migrations
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc"  -delete


# python manage.py collectstatic --noinput