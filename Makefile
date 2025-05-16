.PHONY: test migrate upgrade downgrade run install

install:
	pip install -r requirements.txt

test:
	python -m pytest --disable-pytest-warnings

migrate:
	flask db migrate

upgrade:
	flask db upgrade

downgrade:
	flask db downgrade

run:
	flask run