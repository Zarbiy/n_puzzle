env_python:
	python3 -m venv venv

install_pygame:
	pip install pygame

active_env:
	source venv/bin/activate

deactive_env:
	deactivate