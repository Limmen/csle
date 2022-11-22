
<p align="center">
<img src="docs/csle_logo.png" width="600">
</p>

<p align="center">
    <a href="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green">
        <img src="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green" /></a>
    <a href="https://img.shields.io/badge/version-0.0.1-blue">
        <img src="https://img.shields.io/badge/version-0.0.1-blue" /></a>
</p>
# What is CSLE?

CSLE is a platform for evaluating and developing reinforcement learning agents for control problems in cyber security.
It can be considered as a cyber range specifically designed for reinforcement learning agents. Everything from network
emulation, to simulation and implementation of network commands have been co-designed to provide an environment where it
is possible to train and evaluate reinforcement learning agents on practical problems in cyber security.

<p align="center">
<img src="docs/arch.png" width="600">
</p>

# Main Features

- **Emulations**
    - [x] 50+ pre-defined versions of emulation environments
    - [x] Automatic generation of custom emulation environment
    - [x] Monitoring Framework with Webapp, Grafana, Prometheus, C-advisor, Node-exporter
    - [x] Automatic Network Traffic Simulation
    - [x] 20+ vulnerable containers with exploits

- **Open-AI Gym Environment**
    - [x] GUI rendering
    - [x] optimal stopping game
    - [x] Simulation-mode
    - [x] Emulation-mode

- **Learning Process**
    - [x] Attacker training
    - [x] Defender training
    - [x] Self-play

- **System Identification**
    - [x] Custom system identifification algorithm to learn model of emulation
    - [ ] Function approximation

- **Policy-examination**
    - [x] A System for Inspecting Automated Intrusion Prevention Policies

- **Management and Monitoring**
    - [x] A distributed telemetry system for real-time monitoring
    - [x] A management platform with an extensive REST API and web frontend

## Installation

Installation instructions are available at [Installation](Installation.md)

## Usage

Usage examples are available at [Usage](Usage.md)

## Documentation

TODO

### System Documentation

TODO 

### APIs

See TODO and the README.md files inside each sub-directory:

- **Emulation System** ([emulation-system](./emulation-system)).
- **Simulation System** ([simulation-system](./simulation-system)).
- **Management System** ([management-system](./management-system)).
- **Metastore** ([metastore](./metastore)).
- **General Documentation** ([docs](./docs)).

## Tutorials

TODO

## Demonstrations

[![IMAGE ALT TEXT](http://img.youtube.com/vi/18P7MjPKNDg/0.jpg)](http://www.youtube.com/watch?v=18P7MjPKNDg "A System for Interactive Examination of Learned Security Policies - Hammar & Stadler")

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020-2022, Kim Hammar

## Publications

For a list of publications and citation information see: [Publications](Publications.md)

## See also

- [gym-idsgame](https://github.com/Limmen/gym-idsgame)
- [gym-optimal-intrusion-response](https://github.com/Limmen/gym-optimal-intrusion-response)
- [awesome-rl-for-cybersecurity](https://github.com/Limmen/awesome-rl-for-cybersecurity)

