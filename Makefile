VENV = venv
PYTHON = python3.10
PIP = $(VENV)/bin/pip

run: $(VENV)/bin/activate
	$(VENV)/bin/python manage.py runserver 8080

$(VENV)/bin/activate: requirements.txt
	python3.10 -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf $(VENV)
	find -iname "*pyc" -delete