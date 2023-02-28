.PHONY: clean

all: install_dev install unit_tests tests release

release: build push

install_dev:
	pip install -q build
	python3 -m pip install --upgrade twine
	python -m pip install flake8
	python3 -m pip install -U mypy
	pip install -U pytest mock pytest-mock pytest-cov
	pip install sphinx sphinxcontrib-napoleon sphinx-rtd-theme
	pip install tox

tests:
	tox

unit_tests:
	pytest --cov=gym_csle_intrusion_response_game

types:
	mypy .

lint:
	flake8 .

docs:
	cd docs; sphinx-apidoc -f -o source/ ../gym_csle_intrusion_response_game/ && make html && cp -r build/html ../../../../docs/_docs/gym_csle_intrusion_response_game

install:
	pip install -e .

build:
	python3 -m build

push:
	python3 -m twine upload dist/*

clean:
	rm -r dist