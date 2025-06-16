# Переменные
DOCKER_COMPOSE = docker compose
DOCKER_COMPOSE_FILE = docker-compose.yml

# Загрузка переменных из .env файла
include .env
export

# Основные команды
.PHONY: build up down restart logs init-model clean help

build: ## Собрать все контейнеры
	$(DOCKER_COMPOSE) build

up: ## Запустить все контейнеры
	$(DOCKER_COMPOSE) up -d

down: ## Остановить все контейнеры
	$(DOCKER_COMPOSE) down

restart: down up ## Перезапустить все контейнеры

logs: ## Показать логи контейнеров
	$(DOCKER_COMPOSE) logs -f

init-model: ## Инициализировать модель
	chmod +x init-model.sh
	./init-model.sh

clean: down ## Очистить все контейнеры и volumes
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

# Команды для разработки
dev-install: ## Установить зависимости для разработки
	pip install -r requirements.txt

dev-run: ## Запустить приложение локально
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Команды для тестирования API
test-init: ## Тест инициализации базы знаний
	curl -X POST http://localhost:8000/initialize -H "Content-Type: application/json" -d '["test document 1", "test document 2"]'

test-query: ## Тест запроса к API
	curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"question": "test question"}'

help: ## Показать это сообщение
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# По умолчанию показываем help
.DEFAULT_GOAL := help 