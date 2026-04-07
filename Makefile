.PHONY: format run

format:
	cd backend && venv/bin/ruff format app

run:
	cd backend && venv/bin/uvicorn app.main:app --reload

test: 
	cd backend && venv/bin/python -m pytest
