<p align="center">
<img src="docs/img/csle_logo_cropped.png" width="40%" height="40%">
</p>

<p align="center">
    <a href="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green">
        <img src="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green" /></a>
    <a href="https://img.shields.io/badge/version-0.3.0-blue">
        <img src="https://img.shields.io/badge/version-0.3.0-blue" /></a>
    <a href="https://img.shields.io/badge/Maintained%3F-yes-green.svg">
        <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" /></a>
    <a href="https://limmen.dev/csle">
        <img src="https://img.shields.io/website-up-down-green-red/http/shields.io.svg" /></a>
     <a href="https://ieeexplore.ieee.org/document/9779345">
        <img src="https://zenodo.org/badge/doi/10.1109/TNSM.2022.3176781.svg" /></a>
</p>

# What is the Cyber Security Learning Environment (CSLE)?

CSLE is a platform for evaluating and developing reinforcement learning agents for control problems in cyber security.
It can be considered as a cyber range specifically designed for reinforcement learning agents. Everything from network
emulation, to simulation and implementation of network commands have been co-designed to provide an environment where it
is possible to train and evaluate reinforcement learning agents on practical problems in cyber security.

<p align="center">
<img src="docs/img/arch.png" width="600">
</p>

# Main Features

### **Emulation System**

CLSE includes a system for emulating large scale IT infrastructures, cyber attacks, and client populations. It is based
on Linux containers and can be used to collect traces and to evaluate security policies.

![](docs/img/cli.gif)

### **Simulation System**

CSLE includes a simulation system for executing reinforcement learning algorithms and simulating Markov decision
processes and Markov games. It is built in Python and can be integrated with standard machine learning libraries.

![](docs/img/training.gif)

### **Management System**

CSLE includes a system for managing emulations and simulations which can be accessed either through a REST API or
through a web interface. The management system allows a) to start/stop emulations/simulations; b) real-time monitoring
of emulation and simulation processes; and c), shell access to components of emulations.

![](docs/img/web_ui.gif)

## Documentation

Documentation, installation instructions, and usage examples are available [here](https://limmen.dev/csle/).

## Supported Releases

| Release                                                       | Build Status | Last date of support |
|---------------------------------------------------------------|--------------|----------------------|
| [v.0.3.0](https://github.com/Limmen/csle/releases/tag/v0.3.0) | -            | 2024-01-17           |
| [v.0.2.0](https://github.com/Limmen/csle/releases/tag/v0.2.0) | -            | 2023-10-30           |
| [v.0.1.0](https://github.com/Limmen/csle/releases/tag/v0.1.0) | -            | 2023-06-06           |

Maintenance releases have a stable API and dependency tree, and receive bug fixes and critical improvements but not new
features. We currently support each release for a window of 6 months.

## Supported Platforms

<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/8/8e/OS_X-Logo.svg" width="7%" height="7%"/>

<img src="https://upload.wikimedia.org/wikipedia/commons/3/35/Tux.svg" width="7%" height="7%" style="margin-left:70px;"/>
</p>

## Maintainer

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://limmen.dev"><img src="https://github.com/Limmen.png" width="100px;" alt="Kim Hammar"/><br /><sub><b>Kim Hammar</b></sub></a><br /><kimham@kth.se></td>
    </tr>
  </tbody>
</table>

## Contribute

Contributions are very welcome. Please use Github issues and pull requests. See
the [documentation](https://limmen.dev/csle/) for further instructions.

### List of Contributors :star2:

Thanks go to these people!

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://limmen.dev"><img src="https://github.com/Limmen.png" width="100px;" alt="Kim Hammar"/><br /><sub><b>Kim Hammar</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/arvid123"><img src="https://github.com/arvid123.png" width="100px;" alt="Arvid Lagerqvist"/><br /><sub><b>Arvid Lagerqvist</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nforsg"><img src="https://github.com/nforsg.png" width="100px;" alt="Nils Forsgren"/><br /><sub><b>Nils Forsgren</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/foroughsh"><img src="https://github.com/foroughsh.png" width="100px;" alt="Forough Shahab Samani"/><br /><sub><b>Forough Shahab Samani</b></sub></a></td>
    </tr>
  </tbody>
</table>

Technical advisors: Prof. Rolf Stadler & Prof. Pontus Johnson. 

## Copyright and license

<p>
<a href="./LICENSE.md">Creative Commons (C) 2020-2023, Kim Hammar</a>
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
&nbsp;
and
&nbsp;<a href="https://www.kth.se/cdis" target="_blank">
<img align="absmiddle" src="docs/img/cdis_logo_transparent.png" width="10%" height="10%">
</a>
</p>
