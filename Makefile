.PHONY: format run deploy test db_up db_down db_reload proper-test

ifneq (,$(wildcard .env))
    include .env
    export $(shell sed 's/=.*//' .env)
endif

format:
	venv/bin/ruff format app

run:
	venv/bin/uvicorn app.main:app --reload

deploy:
	$(MAKE) db_up
	$(MAKE) run

test: 
	venv/bin/python -m pytest

db_up:
	docker compose up -d db

db_down:
	docker compose down

db_reload: db_down db_up

proper-test:
	venv/bin/schemathesis run http://localhost:8000/openapi.json \
	  --checks not_a_server_error \
	  -H "Authorization: Bearer $(SCHEMATHESIS_TOKEN)" \
	  --max-examples 5 \
	  --rate-limit 30/s \
	  --exclude-path /users/me/avatar

seed:
	venv/bin/python seed.py

fresh:
	docker compose down -v
	docker compose up -d db
	sleep 15
	venv/bin/alembic upgrade head
	$(MAKE) seed