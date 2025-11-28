.PHONY: help install run migrate makemigrations createsuperuser shell test clean check

PYTHON := $(shell command -v python || command -v python3)

help:
	@echo "Django Todo Application - Available commands:"
	@echo ""
	@echo "  make install        - Install Django dependencies"
	@echo "  make run            - Run development server"
	@echo "  make migrate        - Apply database migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make createsuperuser - Create admin superuser"
	@echo "  make shell          - Open Django shell"
	@echo "  make test           - Run tests"
	@echo "  make check          - Check for project issues"
	@echo "  make clean          - Remove Python cache files and database"
	@echo ""

install:
	pip install django

run:
	$(PYTHON) manage.py runserver

migrate:
	$(PYTHON) manage.py migrate

makemigrations:
	$(PYTHON) manage.py makemigrations

createsuperuser:
	$(PYTHON) manage.py createsuperuser

shell:
	$(PYTHON) manage.py shell

test:
	$(PYTHON) manage.py test

check:
	$(PYTHON) manage.py check

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -f db.sqlite3
	rm -rf todos/migrations/0*.py
	@echo "Cleaned Python cache files and database"
