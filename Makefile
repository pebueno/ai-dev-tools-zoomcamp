.PHONY: help install run migrate makemigrations createsuperuser shell test clean check

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
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

createsuperuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

test:
	python manage.py test

check:
	python manage.py check

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -f db.sqlite3
	rm -rf todos/migrations/0*.py
	@echo "Cleaned Python cache files and database"
