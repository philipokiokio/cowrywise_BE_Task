

PYTHON = venv/bin/python
PIP = venv/bin/pip
BLACK = venv/bin/python -m black
RUFF = venv/bin/python -m ruff 
MESSAGE = "Local Table Migrations"
STEP = 1


venv : 
	python3 -m venv venv
	
activate :
	source /venv/bin/activate

install :
	pip install -r requirements.txt 


local-migration:
	alembic -c local_dev_alembic.ini revision -m "$(MESSAGE)" --autogenerate


local-migrate:
	alembic -c local_dev_alembic.ini upgrade heads



local-migrate-down:
	alembic -c local_dev_alembic.ini downgrade -"$(STEP)"


local-head:
	alembic -c local_dev_alembic.ini heads


start_server:
	uvicorn root.app:app --reload --port=6970 --host=0.0.0.0
	
prod_server:
	alembic upgrade heads && uvicorn root.app:app --port=10000 --host=0.0.0.0

all-test:
	pytest tests

format : 
	$(BLACK) --preview ./project_name

standard:
	$(RUFF) check ./project_name --ignore=E731,E712
