.PHONY: venv, install, clean, help

all: venv install
	@echo "Build success"

venv:
	python3 -m venv .venv

install:
	. .venv/bin/activate; pip3 install -r requirements.txt
	
clean:
	rm -rf .venv
	rm -rf .cache
	rm -rf .log
	find ./data -name "*.db" -type f -delete
	find . -depth -name "__pycache__" -type d -exec rm -rf {} \;

module ?= ''
test: venv install
	. .venv/bin/activate; python3 test/main.py -m $(module)

port ?= 8080
run: venv install
	. .venv/bin/activate; .venv/bin/uvicorn --host 0.0.0.0 --port $(port) main:app

help:
	@echo "Available targets:"
	@echo "  venv    Create a virtual environment"
	@echo "  install Install dependencies"
	@echo "  clean   Remove all build artifacts、venv、 cache、logs and database"
	@echo "  test   Run test cases"
	@echo "  run     Run the application"
