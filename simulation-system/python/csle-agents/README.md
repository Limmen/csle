# `csle-agents`

A library with reinforcement learning algorithms, control-theoreitc algorithms, dynamic programming algorithms,
and game-theoretic algorithms for finding defender policies.

## Requirements

- Python 3.8+
- `csle-common`
- `csle-collector`
- `csle-attacker`
- `csle-defender`
- `csle-system-identification`
- `gym-csle-stopping-game`
- `pulp` (for linear and convex optimization)
- `Bayesian optimization` (for Bayesian optimization algorithms)

## Installation

```bash
# install from pip
pip install csle-agents==<version>
# local install from source
$ pip install -e csle-agents
# force upgrade deps
$ pip install -e csle-agents --upgrade

# git clone and install from source
git clone https://github.com/Limmen/csle
cd csle/simulation-system/python/csle-agents
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

The latest documentation is available at [https://limmen.dev/csle/docs/csle-agents](https://limmen.dev/csle/docs/csle-agents)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../csle_agents/
make html
```
To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle), copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/csle-agents
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

