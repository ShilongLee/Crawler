.PHONY: venv
venv:
	python3 -m venv .venv

.PHONY: install
install:
	. .venv/bin/activate; pip3 install -r requirements.txt

.PHONY: clean
clean:
	rm -rf .venv

port ?= 8080
thread ?= 4
run: venv install
	. .venv/bin/activate; .venv/bin/gunicorn -c config/gunicorn.conf.py -w $(thread) -b :$(port) main:app
