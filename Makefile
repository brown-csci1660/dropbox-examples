PYTHON = python3
PIP = pip

ENV = env

.PHONY: setup-env enter

setup-env:
	$(PYTHON) -m venv $(ENV)
	. $(ENV)/bin/activate;	pip install -r requirements.txt

enter:
	. $(ENV)/bin/activate

test:
	$(PYTHON) -m unittest -v

clean-env:
	rm -rf $(ENV)
	rm -rf __pycache__

