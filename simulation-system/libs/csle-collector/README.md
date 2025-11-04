# `csle-collector`

This library contains scripts and programs for collecting data from the emulation. 

<p align="center">
<img src="docs/data_collection_1.png" width="600">
</p>

[![PyPI version](https://badge.fury.io/py/csle-collector.svg)](https://badge.fury.io/py/csle-collector)
![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-collector)

## Re-generate gRPC files

To re-generate the gRPC files, run: 
```bash
python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/client_manager/. ./protos/client_manager.proto --mypy_out=./src/csle_collector/client_manager/.
python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/kafka_manager/. ./protos/kafka_manager.proto --mypy_out=./src/csle_collector/kafka_manager/.
python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/elk_manager/. ./protos/elk_manager.proto --mypy_out=./src/csle_collector/elk_manager/.
python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/docker_stats_manager/. ./protos/docker_stats_manager.proto --mypy_out=./src/csle_collector/docker_stats_manager/.
python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/snort_ids_manager/. ./protos/snort_ids_manager.proto --mypy_out=./src/csle_collector/snort_ids_manager/.
python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/host_manager/. ./protos/host_manager.proto --mypy_out=./src/csle_collector/host_manager/.
python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/ossec_ids_manager/. ./protos/ossec_ids_manager.proto --mypy_out=./src/csle_collector/ossec_ids_manager/.
python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/traffic_manager/. ./protos/traffic_manager.proto --mypy_out=./src/csle_collector/traffic_manager/.
python -m grpc_tools.protoc -I./protos/ --python_out=./src/csle_collector/. --grpc_python_out=./src/csle_collector/ryu_manager/. ./protos/ryu_manager.proto --mypy_out=./src/csle_collector/ryu_manager/.
```

## Requirements

- Python 3.8+
- `csle-base`
- `grpcio` (for the collector API)
- `grpcio-tools` (for the collector API)
- `scipy` (for statistical models of client processes)
- `confluent-kafka` (for interacting with Kafka)
- `docker` (for interacting with Docker)
- `requests` (for interacting with the Ryu Controller's web interface)
- `netifaces` (networking utility)
- `PyYaml` (for parsing yaml files)
- `pycryptodome` (for cryptographic functions)

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

## Installation

```bash
# install from pip
pip install csle-collector==<version>
# local install from source
$ pip install -e csle-collector
# or (equivalently):
make install
# force upgrade deps
$ pip install -e csle-collector --upgrade
# git clone and install from source
git clone https://github.com/Kim-Hammar/csle
cd csle/simulation-system/libs/csle-collector
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

The latest documentation is available at [https://kim-hammar.github.io/csle//docs/csle-collector](https://kim-hammar.github.io/csle//docs/csle-collector)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../src/csle_collector/
make html
```
To update the official documentation at [https://kim-hammar.github.io/csle/](https://kim-hammar.github.io/csle/), copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/csle-collector
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

To run the unit tests, execute the following command:
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
pytest --cov=csle_collector
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
python3 -m build
# or (equivalently)
make build
```
After running the command above, the built package is available at `./dist`.

Push the built package to PyPi by running:
```bash
python3 -m twine upload dist/*
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