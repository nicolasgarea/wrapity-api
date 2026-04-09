.PHONY: format run deploy test db_up db_down db_reload proper-test

ifneq (,$(wildcard backend/.env))
    include backend/.env
    export $(shell sed 's/=.*//' backend/.env)
endif

format:
	cd backend && venv/bin/ruff format app

run:
	cd backend && venv/bin/uvicorn app.main:app --reload

deploy:
	$(MAKE) db_up
	$(MAKE) run

test: 
	cd backend && venv/bin/python -m pytest

db_up:
	docker compose up -d

db_down:
	docker compose down

db_reload: db_down db_up

proper-test:
	cd backend && venv/bin/schemathesis run http://localhost:8000/openapi.json --checks not_a_server_error -H "Authorization: Bearer $(SCHEMATHESIS_TOKEN)" --max-examples 5
