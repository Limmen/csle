# `csle`: Cyber Security Learning Environment

## A research platform to develop self-learning systems for cyber security using reinforcement learning

`csle` is a platform for evaluating and developing reinforcement learning agents for control problems in cyber security.
It can be considered as a cyber range specifically designed for reinforcement learning agents. Everything from network
emulation, to simulation and implementation of network commands have been co-designed to provide an environment where it
is possible to train and evaluate reinforcement learning agents on practical problems in cyber security.

The platform can be used to implement different use cases. Each use case consist of an emulated infrastructure (used for
evaluation), and a MDP/POMDP/Markov Game interface for training agents. For example, the platform can be used to study
the use case of intrusion prevention and train a reinforcement learning agent to prevent network intrusions by attackers
in real-time.


<p align="center">
    <a href="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green">
        <img src="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green" /></a>
    <a href="https://img.shields.io/badge/version-0.0.1-blue">
        <img src="https://img.shields.io/badge/version-0.0.1-blue" /></a>
</p>

## Outline

* [What is csle?](#what-is-csle)
* [Architecture](#architecture)
* [Features](#features)
* [Quickstart](#quickstart)
* [Documentation](#documentation)
* [Author &amp; Maintainer](#author--maintainer)
* [Copyright and license](#copyright-and-license)
* [Disclaimer](#disclaimer)

## Architecture

The method used in `csle` for learning and validating policies includes two systems. First, we develop an **emulation
system** where key functional components of the target infrastructure are replicated. In this system, we run attack
scenarios and defender responses. These runs produce system metrics and logs that we use to estimate empirical
distributions of infrastructure metrics, which are needed to simulate MDP/POMDP/Markov Game episodes. Second, we develop
a **simulation system** where MDP/POMDP/Markov Game episodes are executed and policies are incrementally learned.
Finally, the policies are extracted and evaluated in the emulation system, and can also be implemented in the target
infrastructure. In short, the emulation system is used to provide the statistics needed to simulate the MDP/POMDP/Markov
Game and to evaluate policies, whereas the simulation system is used to learn policies.


<p align="center">
<img src="docs/arch.png" width="600">
</p>

### Emulation System

The emulation system executes on a cluster of machines that runs a virtualization layer provided by Docker containers
and virtual links. The system emulates the clients, the attacker, the defender, as well as physical components of the
target infrastructure (e.g application servers and gateways). Physical entities are emulated and software functions are
executed in Docker containers of the emulation system. The software functions replicate important components of the
target infrastructure, such as, web servers, databases, and an IDS.

### Simulation System

The simulation system implements a MDP/POMDP/Markov Game that can be used to train defender policies using reinforcement
learning. It exposes an OpenAI-gym interface.

### Management System

The management system allows to track the execution of running emulations and their resource consumptions. It also
includes an operations center where emulations can be managed and learned policies can be examines. Specifically, the
policy examination component of the management system is a component for interactive examination of learned security
policies. It allows a user to traverse episodes of Markov decision processes in a controlled manner and to track the
actions triggered by security policies. Similar to a software debugger, a user can continue or or halt an episode at any
time step and inspect parameters and probability distributions
of interest. The system enables insight into the structure of a given policy and in the behavior of a policy in edge
cases.

## Features

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

Usage examples and guides are available at [Usage](Usage.md)

## Documentation

For documentation, see the README.md files inside each sub-directory,

- **Emulation System** ([emulation-system](./emulation-system)).
- **Simulation System** ([simulation-system](./simulation-system)).
- **Management System** ([management-system](./management-system)).
- **Metastore** ([metastore](./metastore)).
- **General Documentation** ([docs](./docs)).

## Video tutorials

### NOMS22 Demo - A System for Interactive Examination of Learned Security Policies

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

## Disclaimer

All code and software in this repository is for Educational purpose ONLY. Do not use it without permission. The usual
disclaimer applies, especially the fact that me (Kim Hammar) is not liable for any damages caused by direct or indirect
use of the information or functionality provided by these programs. The author or any Internet provider bears NO
responsibility for content or misuse of these programs or any derivatives thereof. By using these programs you accept
the fact that any damage (dataloss, system crash, system compromise, etc.)
caused by the use of these programs is not Kim Hammar's responsibility.
