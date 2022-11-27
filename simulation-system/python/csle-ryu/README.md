# `csle-ryu`

A library with SDN controllers used in CSLE for emulating software-defined networks.

## Requirements

- Python 3.8+
- `ryu` (for HTTP server)
- `eventlet` (for HTTP server)
- `confluent-kafka` (for interacting with Kafka)
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

Install the `flake8` linter:
```bash
python -m pip install flake8
```

Install the mypy for static type checking:
```bash
python3 -m pip install -U mypy
```

Install `pytest` and `mock`:
```bash
pip install -U pytest mock pytest-mock
```

Install Sphinx to automatically generate API documentation from docstrings:
```bash
pip install sphinx sphinxcontrib-napoleon sphinx-rtd-theme
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

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2020-2022, Kim Hammar

