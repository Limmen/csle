# `csle-agents`

A library with reinforcement learning algorithms, control-theoreitc algorithms, dynamic programming algorithms,
and game-theoretic algorithms for finding defender policies.

[![PyPI version](https://badge.fury.io/py/csle-agents.svg)](https://badge.fury.io/py/csle-agents)
![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-agents) 

## Requirements

- Python 3.8+
- `csle-base`
- `csle-common`
- `csle-collector`
- `csle-attacker`
- `csle-cluster`
- `csle-defender`
- `csle-system-identification`
- `gym-csle-stopping-game`
- `gym-csle-apt-game`
- `gym-csle-cyborg`
- `gym-csle-intrusion-response-game`
- `csle-tolerance`
- `pulp` (for linear and convex optimization)
- `Bayesian optimization` (for Bayesian optimization algorithms)
- `iteround` (utility library)
- `emukit` (for Bayesian optimization)
- `cma` (for CMA optimization)

## Development Requirements

- Python 3.8+
- `flake8` (for linting)
- `flake8-rst-docstrings` (for linting docstrings)
- `tox` (for automated testing)
- `pytest` (for unit tests)
- `pytest-cov` (for unit test coverage)
- `mypy` (for static typing)
- `mypy-extensions` (for static typing)
- `mypy-protobuf` (for static typing)
- `types-PyYaml` (for static typing)
- `types-paramiko` (for static typing)
- `types-protobuf` (for static typing)
- `types-requests` (for static typing)
- `types-urllib3` (for static typing)
- `sphinx` (for API documentation)
- `sphinxcontrib-napoleon` (for API documentation)
- `sphinx-rtd-theme` (for API documentation)
- `pytest-mock` (for mocking tests)
- `pytest-grpc` (for grpc tests)

## Installation

```bash
# install from pip
pip install csle-agents==<version>
# local install from source
$ pip install -e csle-agents
# or (equivalently):
make install
# force upgrade deps
$ pip install -e csle-agents --upgrade
# git clone and install from source
git clone https://github.com/Kim-Hammar/csle
cd csle/simulation-system/libs/csle-agents
pip3 install -e .
# Install development dependencies
$ pip install -r requirements_dev.txt
```

### Development tools

Install all development tools at once:
```bash
make install_dev
```
or
```bash
pip install -r requirements_dev.txt
```
## API documentation

This section contains instructions for generating API documentation using `sphinx`.

### Latest Documentation

The latest documentation is available at [https://kim-hammar.github.io/csle//docs/csle-agents](https://kim-hammar.github.io/csle//docs/csle-agents)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../src/csle_agents/
make html
```
To update the official documentation at [https://kim-hammar.github.io/csle/](https://kim-hammar.github.io/csle/), copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/csle-agents
```

To run all documentation commands at once, use the command:
```bash
make docs
```

## Static code analysis

To run the Python linter, execute the following command:
```
flake8 .
# or (equivalently):
make lint
```

To run the mypy type checker, execute the following command:
```
mypy .
# or (equivalently):
make types
```

## Unit tests

To run all the unit tests, execute the following command:
```
pytest
# or (equivalently):
make unit_tests
```

To run tests of a specific test suite, execute the following command:
```
pytest -k "ClassName"
```

To generate a coverage report, execute the following command:
```
pytest --cov=csle_agents
```

## Run tests and code analysis in different python environments

To run tests and code analysis in different python environemnts, execute the following command:

```bash
tox
# or (equivalently):
make tests
```

## Create a new release and publish to PyPi

First build the package by executing:
```bash
python -m build
# or (equivalently)
make build
```
After running the command above, the built package is available at `./dist`.

Push the built package to PyPi by running:
```bash
python -m twine upload dist/*
# or (equivalently)
make push
```

To run all commands for the release at once, execute:
```bash
make release
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020-2025, Kim Hammar

