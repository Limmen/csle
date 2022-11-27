# `csle-cli`

The command-line-interface (CLI) tool for CSLE. 

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
csle start| stop | clean <name>
```

- Open a shell in a given container

```bash
csle shell <container-name>
```

- Remove a container, image, network, emulation, or all

```bash
csle rm <container-name> | <network-name> | <image-name> | <emulation-name> all
```

- Install emulations, simulations, or Docker images

```bash
csle install emulations | simulations | derived_images | base_images | <emulation_name> | <simulation_name> | <derived_image_name> | <base_image_name> | metastore | all
```

- Uninstall emulations, simulations, or Docker images

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

## Requirements

- Python 3.8+
- `click>=8.0.0`
- `csle-common`
- `csle-collector`
- `csle-attacker`
- `csle-defender`
- `csle-system-identification`
- `gym-csle-stopping-game`

## Installation

```bash
# install from pip
pip install csle-cli==<version>
# local install from source
$ pip install -e csle-cli
# force upgrade deps
$ pip install -e csle-cli --upgrade

# git clone and install from source
git clone https://github.com/Limmen/csle
cd csle-cli
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

## API documentation

The latest documentation is available at [https://limmen.dev/csle/docs](https://limmen.dev/csle/docs)

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2020-2022, Kim Hammar

