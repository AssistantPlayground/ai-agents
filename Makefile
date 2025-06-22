include .env
export

.PHONY: build up down restart logs init-model clean help

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart: down up

worker:
	chmod +x worker-start.sh
	./worker-start.sh

test-init:
	curl -X POST http://localhost:8000/initialize -H "Content-Type: application/json" -d '["test document 1", "test document 2"]'

test-query:
	curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"question": "test question"}'
