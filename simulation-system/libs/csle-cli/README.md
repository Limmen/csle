# `csle-cli`

The command-line-interface (CLI) tool for CSLE.

[![PyPI version](https://badge.fury.io/py/csle-agents.svg)](https://badge.fury.io/py/csle-cli)
![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-cli)

## Requirements

- Python 3.8+
- `csle-base`
- `csle-common`
- `csle-cluster`
- `csle-collector`
- `csle-attacker`
- `csle-defender`
- `csle-system-identification`
- `gym-csle-stopping-game`
- `gym-csle-apt-game`
- `gym-csle-cyborg`
- `csle-tolerance`
- `gym-csle-intrusion-response-game`
- `csle-agents`

## Development Requirements

- Python 3.8+
- `flake8` (for linting)
- `flake8-rst-docstrings` (for linting docstrings)
- `tox` (for automated testing)
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

## Quickstart

To see the available commands, run:

```bash
csle --help
```

Examples:

- Initialize management accounts

```bash
csle init
```

- List available containers, emulations, images, and networks:

```bash
csle ls --all
```

- List containers only

```bash
csle ls containers --all
```

- List running containers only

```bash
csle ls containers
```

- List emulations

```bash
csle ls emulations --all
```

- List running emulations only

```bash
csle ls emulations
```

- Inspect a specific emulation/container/image/network

```bash
csle ls <name>
```

- Start/Stop/Clean a specific emulation/container

```bash
csle start | stop | clean <name>
```

- Open a shell in a given container

```bash
csle shell <container-name>
```

- Remove a container, image, network, emulation, or all

```bash
csle rm <container-name> | <network-name> | <image-name> | <emulation-name> all
```

- Install emulations, simulations, the metastore, or Docker images

```bash
csle install emulations | simulations | derived_images | base_images | <emulation_name> | <simulation_name> | <derived_image_name> | <base_image_name> | metastore | all
```

- Uninstall emulations, simulations, the metastore, or Docker images

```bash
csle uninstall emulations | simulations | derived_images | base_images | <emulation_name> | <simulation_name> | <derived_image_name> | <base_image_name> | metastore | all
```

- Start trainnig job with a given id

```bash
csle trainingjob <id>
```

- Start system identification job with a given id

```bash
csle systemidentificationjob <id>
```

- Start data collection job with a given id

```bash
csle datacollectionjob <id>
```

- Start the REST API

```bash
csle start flask
```

- Start grafana

```bash
csle start | stop grafana
```

- Start prometheus

```bash
csle start | stop prometheus
```

- Start cadvisor

```bash
csle start | stop cadvisor
```

- Start node-exporter

```bash
csle start | stop nodeexporter
```

- Start hostmanagers

```bash
csle start | stop hostmanagers
```

- Start hostmanager

```bash
csle start | stop hostmanager
```

- Start clientmanager

```bash
csle start | stop clientmanager
```

- Start snortmanagers

```bash
csle start | stop snortmanagers
```

- Start snortmanager

```bash
csle start | stop snortmanager
```

- Start elkmanager

```bash
csle start | stop elkmanager
```

- Start trafficmanagers

```bash
csle start | stop trafficmanagers
```

- Start trafficmanager

```bash
csle start | stop trafficmanager
```

- Start kafkamanager

```bash
csle start | stop kafkamanager
```

- Start ossecmanagers

```bash
csle start | stop ossecmanagers
```

- Start ossecmanager

```bash
csle start | stop ossecmanager
```
- Start ryumanager

```bash
csle start | stop ryumanager
```

- Start filebeats

```bash
csle start | stop filebeats
```

- Start filebeat

```bash
csle start | stop filebeat
```

- Start metricbeats

```bash
csle start | stop metricbeats
```

- Start metricbeat

```bash
csle start | stop metricbeat
```

- Start heartbeats

```bash
csle start | stop heartbeats
```

- Start heartbeat

```bash
csle start | stop heartbeat
```

- Start packetbeats

```bash
csle start | stop packetbeats
```

- Start packetbeat

```bash
csle start | stop packetbeat
```

## Available Commands

| command                   | description                                                                                                                                                                                          | argument 1                                                                                                                                                                                          | argument 2                                                                   | argument 3 | argument 4    | argument 5 | argument 6 | flags                                                                                                                                                                                                                                                                                                                                                                                 | 
|:--------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------|:-----------|:--------------|:-----------|:-----------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `attacker`                | Opens an attacker shell in the given emulation execution                                                                                                                                             | `emulation_name`                                                                                                                                                                                    | `execution_id`                                                               |            |               |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |
| `clean`                   | Removes a container, a network, an image, all networks, all images, all containers, all traces, or all statistics                                                                                    | `all`,`containers`,`emulations`,`emulation_traces`,`simulation_traces`,`emulation_statistics`,`emulation_executions`,`name`                                                                         | `execution_id`                                                               |            |               |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |
| `em`                      | Extracts status information of a given emulation                                                                                                                                                     | `emulation_name`                                                                                                                                                                                    |                                                                              |            |               |            |            | `--host` (check status of host managers), `--stats` (check status of Docker stats manager), `--kafka` (check status of kafka), `--snortids` (check status of the Snort IDS), `--clients` (check status of client population) `--executions` (check status of executions)                                                                                                              |
| `init`                    | Initializes CSLE and sets up management accounts                                                                                                                                                     |                                                                                                                                                                                                     |                                                                              |            |               |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |
| `install`                 | Installs emulations and simulations in the metastore and creates Docker images                                                                                                                       | `emulations`, `simulations`, `emulation_name`, `simulation_name`, `derived_images`, `base_images`, `metastore`, `all`                                                                               |                                                                              |            |               |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |
| `ls`                      | Lists the set of containers, networks, images, or emulations, or all                                                                                                                                 | `containers`, `networks`, `images`, `emulations`, `all`, `environments`, `prometheus`, `node_exporter`, `cadvisor`, `statsmanager`, `managementsystem`, `simulations`, `emulation_executions`, `hostmanagers`, `clientmanager`, `snortmanagers`, `elkmanager`, `trafficmanagers`, `kafkamanager`, `ossecmanagers`, `ryumanager`, `filebeats`, `metricbeats`, `heartbeats`, `packetbeats`, `logfiles`, `logfile`, `emulation_description`       |                                                                              |            |               |            |            | `--all` (list extended information), `--running` (list running entities only (default)), `--stopped` (list stopped entities only)                                                                                                                                                                                                                                                     |
| `rm`                      | Removes a container, a network, an image, all networks, all images, or all containers                                                                                                                | `network_name`, `container_name`, `image_name`, `networks`, `images`, `containers`                                                                                                                  |                                                                              |            |               |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                         |
| `shell`                   | Command for opening a shell inside a running container                                                                                                                                               | `container_name`                                                                                                                                                                                    |                                                                              |            |               |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |    
| `start`                   | Starts an entity, e.g. a container or the management system                                                                                                                                          | `prometheus`, `node_exporter`, `grafana`, `cadvisor`, `flask`, `nginx`, `docker`, `postgresql`, `container_name`, `emulation_name`, `all`, `statsmanager`, `training_job`, `system_id_job`, `image`, `hostmanagers`, `hostmanager`, `clientmanager`, `snortmanagers`, `snortmanager`, `elkmanager`, `trafficmanagers`, `trafficmanager`, `kafkamanager`, `ossecmanagers`, `ossecmanager`, `ryumanager`, `filebeats`, `filebeat`, `metricbeats`, `metricbeat`, `heartbeats`, `heartbeat`, `packetbeats`, `packetbeat` | `container_name` (if the first argument corresponds to a container image),   |            |               |            |            | `--id` (execution id), `--no_clients` (skip starting client population), `--no_traffic` (skip starting traffic generators), `--no_beats` (skip starting/configuring beats)`, --no_network` (skip creating virtual networks) `--ip` (to start a service on a specific node)                                                                                                            |  
| `start_traffic`           | Starts the traffic and client population on a given emulation                                                                                                                                        | `emulation_name`                                                                                                                                                                                    | `execution_id`                                                               |            |               |            |            | `--mu` (the mu paramter for the service time of the client arrivals), `--lamb` (the lambda parameter of the client arrival process), `--t` (time-step length to measure the arrival process), `--nc` (number of commands per client), `--tsf` (the time scaling factor for non-stationary Poisson processes),`--psf` (the period scaling factor for non-stationary Poisson processes) |
| `statsmanager`            | Starts the statsmanager locally                                                                                                                                                                      | `port`                                                                                                                                                                                              | `log_dir`                                                                    | `log_file` | `max_workers` |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |
| `stop`                    | Stops an entity, e.g. an emulation execution or a container                                                                                                                                          | `emulation_name`, `prometheus`, `node_exporter`, `cadvisor`, `grafana`, `flask`, `nginx`, `docker`, `postgresql`, `container_name`, `statsmanager`, `emulation_executions`, `all`, `hostmanagers`, `hostmanager`, `clientmanager`, `snortmanagers`, `snortmanager`, `elkmanager`, `trafficmanagers`, `trafficmanager`, `kafkamanager`, `ossecmanagers`, `ossecmanager`, `ryumanager`, `filebeats`, `filebeat`, `metricbeats`, `metricbeat`, `heartbeats`, `heartbeat`, `packetbeats`, `packetbeat`                   | `execution_id`                                                               |            |               |            |            | `--ip` (to stop a service on a specific node)                                                                                                                                                                                                                                                                                                                                         |
| `stop_traffic`            | Stops the traffic and client population on a given emulation                                                                                                                                         | `emulation_name`                                                                                                                                                                                    | `execution_id`                                                               |            |               |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |
| `systemidentificationjob` | Starts a systemidentification job with the given id                                                                                                                                                  | `job_id`                                                                                                                                                                                            |                                                                              |            |               |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |
| `trainingjob`             | Starts a training job with the given id                                                                                                                                                              | `job_id`                                                                                                                                                                                            |                                                                              |            |               |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |
| `datacollectionjob`       | Starts a data collection job with the given id                                                                                                                                                       | `job_id`                                                                                                                                                                                            |                                                                              |            |               |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |
| `uninstall`               | Uninstall emulations and simulations from the metastore and removes Docker images                                                                                                                    | `emulations`, `simulations`, `emulation_name`, `simulation_name`, `derived_images`, `base_images`, `metastore`, `all`                                                                               |                                                                              |            |               |            |            |                                                                                                                                                                                                                                                                                                                                                                                       |

## Requirements

- Python 3.8+
- `click>=8.0.0`
- `csle-common`
- `csle-cluster`
- `csle-collector`
- `csle-attacker`
- `csle-defender`
- `csle-system-identification`
- `gym-csle-stopping-game`
- `csle-agents`

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
pip install csle-cli==<version>
# local install from source
$ pip install -e csle-cli
# or (equivalently):
make install
# force upgrade deps
$ pip install -e csle-cli --upgrade
# git clone and install from source
git clone https://github.com/Kim-Hammar/csle
cd csle-cli
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

The latest documentation is available at [https://kim-hammar.github.io/csle//docs](https://kim-hammar.github.io/csle//docs)

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

## Integration tests

To run the integration tests, execute the following command:

```
pytest
# or (equivalently):
make unit_tests
```

To generate a coverage report, execute the following command:

```
pytest --cov=csle_cli
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

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2020-2025, Kim Hammar

