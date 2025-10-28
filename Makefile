env_python:
	python3 -m venv venv

install_pygame:
	pip install pygame

install_qt:
	pip install pyqt6
	pip install pyqt6-plugins

active_env:
	source venv/bin/activate

deactive_env:
	deactivate