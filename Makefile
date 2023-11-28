SHELL := /bin/bash
PYTHON := python3
PROJECT_NAME := challenge
VENV_DIR := venv

# Virtual environment
venv:
	virtualenv venv -p $(PYTHON)
	source $(VENV_DIR)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

# Linting
lint: venv
	isort .
	flake8 api

# Build the applications
build:
	docker compose build

# Run the applications
run: build
	docker compose up web -d

# Clean up
clean:
	rm -rf $(VENV_DIR)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

security: venv
	safety check

.PHONY: venv format lint test run clean