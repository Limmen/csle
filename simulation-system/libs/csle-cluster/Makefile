.PHONY: clean

all: install_dev install unit_tests tests release

release: build push

install_dev:
	pip install -r requirements_dev.txt

tests:
	tox

unit_tests:
	pytest --cov=csle_cluster

types:
	mypy .

lint:
	flake8 .

docs:
	cd docs; sphinx-apidoc -f -o source/ ../src/ && make html && cp -r build/html ../../../../docs/_docs/csle-cluster

install:
	pip install -e .

build:
	python3 -m build

push:
	python3 -m twine upload dist/*

clean:
	rm -r dist