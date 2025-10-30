env_python:
	python3 -m venv venv

install_element:
	mkdir -p patern
	source venv/bin/activate
	pip install -r req.txt

deactive_env:
	deactivate