.PHONY: clean

all: install_dev install unit_tests tests release

release: build push

install_dev:
	pip install -r requirements_dev.txt

tests:
	tox

unit_tests:
	pytest --cov=csle_attack_profiler

types:
	mypy .

lint:
	flake8 .

docs:
	cd docs; sphinx-apidoc -f -o source/ ../src/ && make html && cp -r build/html ../../../../docs/_docs/csle-attack-profiler

install:
	pip install -e .

build:
	python -m build

push:
	python -m twine upload dist/*

clean:
	rm -r dist