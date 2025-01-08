# Simulation system

This folder contains python projects that implement the functionality of the simulation system.

- **csle-base** ([csle-base](./csle-base)):
  - [![PyPI version](https://badge.fury.io/py/csle-base.svg)](https://badge.fury.io/py/csle-base)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-base)
  - Contains base classes and definitions for the other CSLE libraries

- **csle-collector** ([csle-collector](./csle-collector)):
  - Contains functionality for sensors and collecting data from nodes in the emulation
  - [![PyPI version](https://badge.fury.io/py/csle-collector.svg)](https://badge.fury.io/py/csle-collector)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-collector)

- **csle-common** ([csle-common](./csle-common)):
    - [![PyPI version](https://badge.fury.io/py/csle-common.svg)](https://badge.fury.io/py/csle-common)
    - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-common)
    - Contains common functionality to all python environments

- **csle-attacker** ([csle-attacker](./csle-attacker)):
  - [![PyPI version](https://badge.fury.io/py/csle-attacker.svg)](https://badge.fury.io/py/csle-attacker)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-attacker)
  - Contains code for emulating attacker actions

- **csle-defender** ([csle-defender](./csle-defender)):
  - [![PyPI version](https://badge.fury.io/py/csle-defender.svg)](https://badge.fury.io/py/csle-defender)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-defender)
  - Contains code for emulating defender actions
    
- **gym-csle-stopping-game** ([gym-csle-stopping-game](./gym-csle-stopping-game)):
    - [![PyPI version](https://badge.fury.io/py/gym-csle-stopping-game.svg)](https://badge.fury.io/py/gym-csle-stopping-game)
    - ![PyPI - Downloads](https://img.shields.io/pypi/dm/gym-csle-stopping-game)
    - A gym environment for an optimal stopping game

- **csle-ryu** ([csle-ryu](./csle-ryu)):
  - [![PyPI version](https://badge.fury.io/py/csle-ryu.svg)](https://badge.fury.io/py/csle-ryu)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-ryu)
  - A library with RYU SDN controllers

- **csle-rest-api** ([csle-rest-api](./csle-rest-api)):
  - [![PyPI version](https://badge.fury.io/py/csle-rest-api.svg)](https://badge.fury.io/py/csle-rest-api)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-rest-api)
  - The CSLE REST API for the management platform

- **csle-agents** ([csle-agents](./csle-agents)):
  - Implementation of control, learning, and game-theoretic algorithms for finding defender policies
  - [![PyPI version](https://badge.fury.io/py/csle-agents.svg)](https://badge.fury.io/py/csle-agents)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-agents)

- **csle-system-identification** ([csle-system-identification](./csle-system-identification)):
  - [![PyPI version](https://badge.fury.io/py/csle-system-identification.svg)](https://badge.fury.io/py/csle-system-identification)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-system-identification)
  - Implementation of system identification algorithms to learn system models based on measured data and traces

- **csle-cli** ([csle-cli](./csle-cli)):
  - [![PyPI version](https://badge.fury.io/py/csle-cli.svg)](https://badge.fury.io/py/csle-cli)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-cli)
  - The CSLE command-line interface

- **csle-cluster** ([csle-cluster](./csle-cluster)):
  - [![PyPI version](https://badge.fury.io/py/csle-cluster.svg)](https://badge.fury.io/py/csle-cluster)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-cluster)
  - The CSLE cluster manager
  
- **gym-csle-intrusion-response-game** ([gym-csle-intrusion-response-game](./gym-csle-intrusion-response-game)):
  - [![PyPI version](https://badge.fury.io/py/gym-csle-intrusion-response-game.svg)](https://badge.fury.io/py/gym-csle-intrusion-response-game)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/gym-csle-intrusion-response-game)
  - A gym environment for an intrusion response game

- **csle-tolerance** ([csle-tolerance](./csle-tolerance)):
  - [![PyPI version](https://badge.fury.io/py/csle-tolerance.svg)](https://badge.fury.io/py/csle-tolerance)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-tolerance)
  - An intrusion-tolerant system: Tolerance: (T)w(o)-(l)ev(e)l (r)ecovery (a)nd respo(n)se (c)ontrol with f(e)edback.

- **gym-csle-apt-game** ([gym-csle-apt-game](./gym-csle-apt-game)):
  - [![PyPI version](https://badge.fury.io/py/gym-csle-apt-game.svg)](https://badge.fury.io/py/gym-csle-apt-game)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/gym-csle-apt-game)
  - A gym environment for an APT Dynkin game

- **gym-csle-cyborg** ([gym-csle-cyborg](./gym-csle-cyborg)):
  - [![PyPI version](https://badge.fury.io/py/gym-csle-cyborg.svg)](https://badge.fury.io/py/gym-csle-cyborg)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/gym-csle-cyborg)
  - A gym environment wrapper for CybORG

- **csle-attack-profiler** ([csle-attack-profiler](./csle-attack-profiler)):
  - [![PyPI version](https://badge.fury.io/py/csle-attack-profiler.svg)](https://badge.fury.io/py/csle-attack-profiler)
  - ![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-attack-profiler)
  - An attack profiler for CSLE based on MITRE ATT&CK

## Commands
To generate API docs, execute:
```bash
./generate_docs.sh
```

To run unit tests, execute:
```bash
./unit_tests.sh
```

To run the type checker, execute:
```bash
./type_checker.sh
```

To make a new Python release, execute:
```bash
python make_release.py
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../LICENSE.md)

Creative Commons

(C) 2020-2025, Kim Hammar