# `gym-csle-stopping-game`

An OpenAI gym reinforcement learning environment that represents the optimal stopping game described in 
[Intrusion Prevention Through Optimal Stopping](https://ieeexplore.ieee.org/document/9779345) and
[Learning Security Strategies through Game Play and Optimal Stopping](https://limmen.dev/assets/papers/icml_ml4cyber_Hammar_Stadler_final_24_june_2022.pdf)

## Requirements

- Python 3.8+
- `csle-common`
- `csle-attacker`
- `csle-csle-defender`
- `csle-collector`

## Installation

```bash
# install from pip
pip install gym-csle-stopping-game==<version>
# local install from source
$ pip install -e gym-csle-stopping-game
# force upgrade deps
$ pip install -e gym-csle-stopping-game --upgrade

# git clone and install from source
git clone https://github.com/Limmen/csle
cd csle/simulation-system/python/gym-csle-stopping-game
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
pip install -U pytest mock pytest-mock pytest-cov
```

Install Sphinx to automatically generate API documentation from docstrings:
```bash
pip install sphinx sphinxcontrib-napoleon sphinx-rtd-theme
```

## API documentation

This section contains instructions for generating API documentation using `sphinx`.

### Latest Documentation

The latest documentation is available at [https://limmen.dev/csle/docs/gym-csle-stopping-game](https://limmen.dev/csle/docs/gym-csle-stopping-game)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../gym_csle_stopping_game/
make html
```
To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle),
copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/gym-csle-stopping-game
```

## Installation & Tests

```bash
# install from pip
pip install gym-csle-stopping-game==1.0.0
# local install from source
$ pip install -e gym-csle-stopping-game
# force upgrade deps
$ pip install -e gym-csle-stopping-game --upgrade

# git clone and install from source
git clone https://github.com/Limmen/csle
csle/simulation-system/gym-csle-stopping-game
pip3 install -e .
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
pytest --cov=gym_csle_stopping_game
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2020-2022, Kim Hammar