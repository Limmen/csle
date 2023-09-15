.PHONY: clean

all: install_dev install unit_tests tests release

release: build push

install_dev:
    pip install -r requirements_dev.txt

tests:
	tox

unit_tests:
	pytest --cov=csle_tolerance

types:
	mypy .

lint:
	flake8 .

docs:
	cd docs; sphinx-apidoc -f -o source/ ../csle_tolerance/ && make html && cp -r build/html ../../../../docs/_docs/csle_tolerance

install:
	pip install -e .

build:
	python3 -m build

push:
	python3 -m twine upload dist/*

clean:
	rm -r dist