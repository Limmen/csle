<p align="center">
<img src="docs/img/csle_logo_cropped.png" width="40%" height="40%">
</p>

<p align="center">
    <a href="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green">
        <img src="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green" /></a>
    <a href="https://img.shields.io/badge/version-0.7.0-blue">
        <img src="https://img.shields.io/badge/version-0.7.0-blue" /></a>
    <a href="https://img.shields.io/badge/Maintained%3F-yes-green.svg">
        <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" /></a>
    <a href="https://limmen.dev/csle">
        <img src="https://img.shields.io/website-up-down-green-red/http/shields.io.svg" /></a> 
     <a href="https://ieeexplore.ieee.org/document/9779345">
        <img src="https://zenodo.org/badge/doi/10.1109/TNSM.2022.3176781.svg" /></a>
     <a href="https://www.youtube.com/watch?v=iE2KPmtIs2A&" alt="youtube"> 
        <img src="https://img.shields.io/badge/Youtube-red.svg?logo=Youtube" /></a>
    <a href="https://arxiv.org/abs/2309.03292">
        <img src="https://img.shields.io/badge/arxiv-2309.03292-silver" alt="Paper">
    </a> 
    <a href="https://github.com/limmen/csle">
     <img src="https://img.shields.io/badge/-github-teal?logo=github" alt="github">
    </a>
    <a href="https://hub.docker.com/r/kimham/csle_cve_2010_0426_base/">
        <img src="https://badgen.net/docker/pulls/kimham/csle_cve_2010_0426_base?icon=docker&label=pulls" 
        alt="Docker pulls">
    </a>
    <a href="https://pypi.org/user/Limmen/">
        <img src="https://img.shields.io/pypi/dm/csle-collector" alt="PyPi downloads">
    </a>
    <a href="https://codecov.io/gh/Limmen/csle" > 
        <img src="https://codecov.io/gh/Limmen/csle/graph/badge.svg?token=YOV2SEDZWF"/> 
    </a>
</p>
<!---
img src="https://badges.toozhao.com/badges/01HCESS7WXTT0T5ANET1CG9GDY/blue.svg" alt="Count">
-->

# The Cyber Security Learning Environment (CSLE)

CSLE is a platform for evaluating and developing reinforcement learning agents for control problems in cyber security.
It can be considered as a cyber range specifically designed for reinforcement learning agents. Everything from network
emulation, to simulation and implementation of network commands have been co-designed to provide an environment where it
is possible to train and evaluate reinforcement learning agents on practical problems in cyber security. The platform
can also be used to combine reinforcement learning with other quantitative methods, e.g., dynamic programming,
computational game theory, evolutionary methods, causal inference, and general optimization.

<p align="center">
<img src="docs/img/arch.png" width="600">
</p>

# Main Features

### 🖥️ **Emulation System**

CLSE includes a system for emulating large scale IT infrastructures, cyber attacks, and client populations. It is based
on Linux containers and can be used to collect traces and to evaluate security policies.

![](docs/img/cli.gif)

> **Note**
> The emulation system is mainly designed to run on a distributed system, e.g., a compute cluster.
> It can run on a laptop as well, but then only small emulations can be created.

### 💭 **Simulation System**

CSLE includes a simulation system for executing reinforcement learning algorithms and simulating Markov decision
processes and Markov games. It is built in Python and can be integrated with standard machine learning libraries.

![](docs/img/training.gif)

> **Note**
> The simulations are compatible with OpenAI Gym/Gymnasium. Hence you can integrate the simulations
> with your own implementations of reinforcement learning algorithms.

### ⚙️ **Management System**

CSLE includes a system for managing emulations and simulations which can be accessed either through Command-Line
Interface (CLI), through a REST API, through Python libraries, or through a web interface. The management system allows
a) to start/stop emulations/simulations; b) real-time monitoring of emulation and simulation processes; and c), shell
access to components of emulations.

![](docs/img/web_ui.gif)

## 🎓 Documentation

Documentation, installation instructions, and usage examples are available [here](https://limmen.dev/csle/). A PDF
version of the documentation is available [here](./releases/).
A video walkthrough of the installation process is available [here](https://www.youtube.com/watch?v=l_g3sRJwwhc).

## 📋 Supported Releases

| Release                                                       | Last date of support |
|---------------------------------------------------------------|----------------------|
| [v.0.7.0](https://github.com/Limmen/csle/releases/tag/v0.7.0) | 2025-03-01           |
| [v.0.6.0](https://github.com/Limmen/csle/releases/tag/v0.6.0) | ~~2024-12-24~~       |
| [v.0.5.0](https://github.com/Limmen/csle/releases/tag/v0.5.0) | ~~2024-06-02~~       |
| [v.0.4.0](https://github.com/Limmen/csle/releases/tag/v0.4.0) | ~~2024-02-07~~       |
| [v.0.3.0](https://github.com/Limmen/csle/releases/tag/v0.3.0) | ~~2024-01-17~~       |
| [v.0.2.0](https://github.com/Limmen/csle/releases/tag/v0.2.0) | ~~2023-10-30~~       |
| [v.0.1.0](https://github.com/Limmen/csle/releases/tag/v0.1.0) | ~~2023-06-06~~       |

Maintenance releases have a stable API and dependency tree, and receive bug fixes and critical improvements but not new
features. We currently support each release for a window of 6 months.

## 📈 Build Status

| Workflow                                                                                                                                     | Status                                                                                                                  |
|----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| [csle-agents](https://github.com/Limmen/csle/actions/workflows/python-csle-agents-build.yml)                                                 | ![status](https://github.com/Limmen/csle/actions/workflows/python-csle-agents-build.yml/badge.svg)                      |
| [csle-attacker](https://github.com/Limmen/csle/actions/workflows/python-csle-attacker-build.yml)                                             | ![status](https://github.com/Limmen/csle/actions/workflows/python-csle-attacker-build.yml/badge.svg)                    |
| [csle-collector](https://github.com/Limmen/csle/actions/workflows/python-csle-collector-build.yml)                                           | ![status](https://github.com/Limmen/csle/actions/workflows/python-csle-collector-build.yml/badge.svg)                   |
| [csle-common](https://github.com/Limmen/csle/actions/workflows/python-csle-common-build.yml)                                                 | ![status](https://github.com/Limmen/csle/actions/workflows/python-csle-common-build.yml/badge.svg)                      |
| [csle-defender](https://github.com/Limmen/csle/actions/workflows/python-csle-defender-build.yml)                                             | ![status](https://github.com/Limmen/csle/actions/workflows/python-csle-defender-build.yml/badge.svg)                    |
| [csle-ryu](https://github.com/Limmen/csle/actions/workflows/python-csle-ryu-build.yml)                                                       | ![status](https://github.com/Limmen/csle/actions/workflows/python-csle-ryu-build.yml/badge.svg)                         |
| [csle-base](https://github.com/Limmen/csle/actions/workflows/python-csle-base-build.yml)                                                     | ![status](https://github.com/Limmen/csle/actions/workflows/python-csle-base-build.yml/badge.svg)                        |
| [csle-system-identification](https://github.com/Limmen/csle/actions/workflows/python-csle-system-identification-build.yml)                   | ![status](https://github.com/Limmen/csle/actions/workflows/python-csle-system-identification-build.yml/badge.svg)       |
| [gym-csle-stopping-game-build](https://github.com/Limmen/csle/actions/workflows/python-gym-csle-stopping-game-build.yml)                     | ![status](https://github.com/Limmen/csle/actions/workflows/python-gym-csle-stopping-game-build.yml/badge.svg)           |
| [gym-csle-intrusion-response-game-build](https://github.com/Limmen/csle/actions/workflows/python-gym-csle-intrusion-response-game-build.yml) | ![status](https://github.com/Limmen/csle/actions/workflows/python-gym-csle-intrusion-response-game-build.yml/badge.svg) |
| [python-linter](https://github.com/Limmen/csle/actions/workflows/python-linter.yml)                                                          | ![status](https://github.com/Limmen/csle/actions/workflows/python-linter.yml/badge.svg)                                 |
| [csle-tolerance-build](https://github.com/Limmen/csle/actions/workflows/python-csle-tolerance-build.yml)                                     | ![status](https://github.com/Limmen/csle/actions/workflows/python-csle-tolerance-build.yml/badge.svg)                   |
| [gym-csle-apt-game-build](https://github.com/Limmen/csle/actions/workflows/python-gym-csle-apt-game-build.yml)                               | ![status](https://github.com/Limmen/csle/actions/workflows/python-gym-csle-apt-game-build.yml/badge.svg)                |
| [gym-csle-cyborg-build](https://github.com/Limmen/csle/actions/workflows/python-gym-csle-cyborg-build.yml)                                   | ![status](https://github.com/Limmen/csle/actions/workflows/python-gym-csle-cyborg-build.yml/badge.svg)                  |
| [csle-attack-profiler-build](https://github.com/Limmen/csle/actions/workflows/python-csle-attack-profiler-build.yml)                         | ![status](https://github.com/Limmen/csle/actions/workflows/python-csle-attack-profiler-build.yml/badge.svg)             |
| [management-system](https://github.com/Limmen/csle/actions/workflows/js-management-system-build)                                             | ![status](https://github.com/Limmen/csle/actions/workflows/js-management-system-build.yml/badge.svg)                    |

## Supported Platforms

<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/8/8e/OS_X-Logo.svg" width="7%" height="7%"/>

<img src="https://upload.wikimedia.org/wikipedia/commons/3/35/Tux.svg" width="7%" height="7%" style="margin-left:70px;"/>
</p>

## Datasets

A dataset of 6400 intrusion traces can be found [here](https://zenodo.org/records/10234379).

## Maintainer

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://limmen.dev"><img src="https://github.com/Limmen.png" width="100px;" alt="Kim Hammar"/><br /><sub><b>Kim Hammar</b></sub></a><br /><kimham@kth.se></td>
    </tr>
  </tbody>
</table>

## 🧑‍🤝‍🧑 Contribute

Contributions are very welcome. Please use GitHub issues and pull requests. See
the [documentation](https://limmen.dev/csle/) for further instructions.

### List of Contributors :star2:

Thanks go to these people!

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://limmen.dev"><img src="https://github.com/Limmen.png" width="100px;" alt="Kim Hammar"/><br /><sub><b>Kim Hammar</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.kth.se/profile/stadler"><img src="https://www.kth.se/files/avatar/stadler.jpeg" width="100px;" alt="Rolf Stadler"/><br /><sub><b>Rolf Stadler</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.kth.se/profile/pontusj"><img src="https://www.kth.se/files/avatar/pontusj.jpeg" width="100px;" alt="Pontus Johnson"/><br /><sub><b>Pontus Johnson</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/FredericoNesti"><img src="https://github.com/FredericoNesti.png" width="100px;" alt="Antonio Frederico Nesti Lopes"/><br /><sub><b>Antonio Frederico Nesti Lopes</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://se.linkedin.com/in/jakob-stymne"><img src="https://media.licdn.com/dms/image/D4D03AQFZ6TfYDIob5Q/profile-displayphoto-shrink_800_800/0/1673357973617?e=2147483647&v=beta&t=MR6uDgRDFcgvHzuMaTNW2SUpf3Hx4T2Spy9e4RpplLw" width="100px;" alt="Jakob Stymne"/><br /><sub><b>Jakob Stymne</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/arvid123"><img src="https://github.com/arvid123.png" width="100px;" alt="Arvid Lagerqvist"/><br /><sub><b>Arvid Lagerqvist</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nforsg"><img src="https://github.com/nforsg.png" width="100px;" alt="Nils Forsgren"/><br /><sub><b>Nils Forsgren</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/foroughsh"><img src="https://github.com/foroughsh.png" width="100px;" alt="Forough Shahab Samani"/><br /><sub><b>Forough Shahab Samani</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ppplbngth"><img src="https://github.com/ppplbngth.png" width="100px;" alt="Bength Roland Pappila"/><br /><sub><b>Bength Roland Pappila</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Yuhu-kth"><img src="https://github.com/Yuhu-kth.png" width="100px;" alt="Yu Hu"/><br /><sub><b>Yu Hu</b></sub></a></td>
    </tr>
    <tr>
       <td align="center" valign="top" width="14.28%"><a href="https://github.com/kingxiaofire"><img src="https://github.com/kingxiaofire.png" width="100px;" alt="Yan Wang"/><br /><sub><b>Yan Wang</b></sub></a></td>
       <td align="center" valign="top" width="14.28%"><a href="https://github.com/Awsnaser"><img src="https://github.com/Awsnaser.png" width="100px;" alt="Aws Jaber"/><br /><sub><b>Aws Jaber</b></sub></a></td>
    </tr>
  </tbody>
</table>

## 🔖 Copyright and license

<p>
<a href="./LICENSE.md">Creative Commons (C) 2020-2025, Kim Hammar</a>
</p>

<p align="center">

</p>

<p align="center">


</p>

## See also

- [gym-idsgame](https://github.com/Limmen/gym-idsgame)
- [gym-optimal-intrusion-response](https://github.com/Limmen/gym-optimal-intrusion-response)
- [awesome-rl-for-cybersecurity](https://github.com/Limmen/awesome-rl-for-cybersecurity)

---
<p align="center" style="align-items:center; display:inline-block">
Made with &#10084; &nbsp;
at &nbsp; <a href="https://www.kth.se/" target="_blank">
<img align="absmiddle" src="docs/img/kth_logo.png" width="10%" height="10%">
</a>
&nbsp;,
&nbsp;<a href="https://www.kth.se/cdis" target="_blank">
<img align="absmiddle" src="docs/img/cdis_logo_transparent.png" width="10%" height="10%">
</a>
and
&nbsp;<a href="https://www.darpa.mil/program/cyber-agents-for-security-testing-and-learning-environments" target="_blank">
<img align="absmiddle" src="docs/img/darpa.png" width="10%" height="10%">
</a>
</p>
