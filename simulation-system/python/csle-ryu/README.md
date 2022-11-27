# `csle-ryu`

A library with SDN controllers used in CSLE for emulating software-defined networks.

[![PyPI version](https://badge.fury.io/py/csle-ryu.svg)](https://badge.fury.io/py/csle-ryu)
![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-ryu)

## Requirements

- Python 3.8+
- `ryu` (for HTTP server)
- `eventlet` (for HTTP server)
- `confluent-kafka` (for interacting with Kafka)

## Development Requirements

- Python 3.8+
- `flake8` (for linting)
- `tox` (for automated testing)
- `pytest` (for unit tests)
- `pytest-cov` (for unit test coverage)
- `mypy` (for static typing)
- `sphinx` (for API documentation)
- `sphinxcontrib-napoleon` (for API documentation)
- `sphinx-rtd-theme` (for API documentation)

## Installation

```bash
# install from pip
pip install csle-ryu==<version>
# local install from source
$ pip install -e csle-ryu
# force upgrade deps
$ pip install -e csle-ryu --upgrade

# git clone and install from source
git clone https://github.com/Limmen/csle
cd csle/simulation-system/python/csle-ryu
pip3 install -e .
```

### Development tools 

Install the Python build tool
```bash
pip install -q build
```

Install `twine` for publishing the package to PyPi:
```bash
python3 -m pip install --upgrade twine
```

Install the `flake8` linter:
```bash
python -m pip install flake8
```

Install the mypy for static type checking:
```bash
python3 -m pip install -U mypy
```

Install `pytest` and `mock` for unit tests:
```bash
pip install -U pytest mock pytest-mock pytest-cov
```

Install Sphinx to automatically generate API documentation from docstrings:
```bash
pip install sphinx sphinxcontrib-napoleon sphinx-rtd-theme
```

Install tox for automatically running tests in different python environments:
```bash
pip install tox
```

## API documentation

This section contains instructions for generating API documentation using `sphinx`.

### Latest Documentation

The latest documentation is available at [https://limmen.dev/csle/docs/csle-ryu](https://limmen.dev/csle/docs/csle-ryu)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../csle_ryu/
make html
```
To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle), 
copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/csle-ryu
```

## Static code analysis

To run the Python linter, execute the following command:
```
flake8 .
```

To run the mypy type checker, execute the following command:
```
mypy .
```

## Unit tests

To run the unit tests, execute the following command:
```
pytest
```

To generate a coverage report, execute the following command:
```
pytest --cov=csle_ryu
```

## Run tests and code analysis in different python environments

To run tests and code analysis in different python environemnts, execute the following command:

```bash
tox
```

## Create a new release and publish to PyPi

First build the package by executing:
```bash
python3 -m build
```
After running the command above, the built package is available at `./dist`.

Push the built package to PyPi by running:
```bash
python3 -m twine upload dist/*
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020-2022, Kim Hammar

