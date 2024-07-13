.PHONY: venv, install, clean, help

venv:
	python3 -m venv .venv

install:
	. .venv/bin/activate; pip3 install -r requirements.txt
	
clean:
	rm -rf .venv

port ?= 10002
run: venv install
	. .venv/bin/activate; .venv/bin/uvicorn --host 0.0.0.0 --port $(port) main:app

help:
	@echo "Available targets:"
	@echo "  venv    Create a virtual environment"
	@echo "  install Install dependencies"
	@echo "  clean   Remove the virtual environment"
	@echo "  run     Run the application"
