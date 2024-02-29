VENV = venv
DEV_VENV = dev_venv
PYTHON = python3.10
PIP = $(VENV)/bin/pip
DEV_PIP = $(DEV_VENV)/bin/pip
PORT = 8080

run: $(VENV)/bin/activate
	$(VENV)/bin/python manage.py runserver $(PORT)

$(VENV)/bin/activate: requirements.txt
	python3.10 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run_dev: $(DEV_VENV)/bin/activate
	$(DEV_VENV)/bin/python manage.py runserver $(PORT)

$(DEV_VENV)/bin/activate: requirements.txt requirements_dev.txt
	python3.10 -m venv $(DEV_VENV)
	$(DEV_PIP) install -r requirements.txt -r requirements_dev.txt

install: $(DEV_VENV)/bin/activate $(VENV)/bin/activate
	python3.10 -m venv $(DEV_VENV)
	$(DEV_PIP) install -r requirements.txt -r requirements_dev.txt
	python3.10 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	
clean:
	rm -rf $(VENV) $(DEV_VENV)
	find -iname "*pyc" -delete