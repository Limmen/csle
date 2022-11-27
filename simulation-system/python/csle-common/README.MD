# `csle-common`

`csle-common` is a library with common functionality for all use-cases implemented in
CSLE. 

## Requirements

- Python 3.8+
- `gym` (for creating RL environments)
- `pyglet` (OpenGL 3D graphics)
- `numpy` (for scientific computing)
- `torch` (for baseline algorithms)
- `docker` (for interacting with the emulations)
- `paramiko` (for SSH tunnels)
- `stable-baselines3` (for baseline RL algorithms)
- `scp` (for SSH copying)
- `random_username` (for auto generating emulations)
- `sphinx` (for API documentation)
- `sphinxcontrib-napoleon` (for API documentation)
- `sphinx-rtd-theme` (for API documentation)
- `psycopg` (to interact with the metastore)
- `click` (for the command line interface)
- `flask` (for the management system Web UI)
- `waitress` (for the management system Web UI)
- `csle-collector` (for data collection and telemetry)
- `psutil` (for command line tasks)
- `csle-ryu` (for SDN network management)

## Installation

```bash
# install from pip
pip install csle-common==<version>
# local install from source
$ pip install -e csle-common
# force upgrade deps
$ pip install -e csle-common --upgrade

# git clone and install from source
git clone https://github.com/Limmen/csle
cd csle/simulation-system/python/csle-common
pip3 install -e .
```

### Development tools

Install the `flake8` linter:
```bash
python -m pip install flake8
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

The latest documentation is available at [https://limmen.dev/csle/docs/csle-common](https://limmen.dev/csle/docs/csle-common)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../csle_common/
make html
```
To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle), copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/csle-common
```

## Static code analysis

To run the static code analysis, execute the following command:
```
flake8 .
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

(C) 2021, Kim Hammar