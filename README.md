
<p align="center">
<img src="docs/img/csle_logo_cropped.png" width="40%", height="40%">
</p>

<p align="center">
    <a href="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green">
        <img src="https://img.shields.io/badge/license-CC%20BY--SA%204.0-green" /></a>
    <a href="https://img.shields.io/badge/version-0.0.1-blue">
        <img src="https://img.shields.io/badge/version-0.0.1-blue" /></a>
    <a href="https://img.shields.io/badge/Maintained%3F-yes-green.svg">
        <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" /></a>
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

CLSE includes a system for emulating large scale IT infrastructures, cyber attacks, and client populations.
It is based on Linux containers and can be used to collect traces and to evaluate security policies. 

### **Simulation System**

CSLE includes a simulation system for executing reinforcement learning algorithms 
and simulating Markov decision processes and Markov games. It is built in Python and can be integrated 
with standard machine learning libraries.

### **Management System**

CSLE includes a system for managing emulations and simulations which can be accessed either through a REST API 
or through a web interface. The management system allows a) to start/stop emulations/simulations; 
b) real-time monitoring of emulation and simulation processes; and c), shell access to components of emulations.

## Documentation

Documentation, installation instructions, and usage examples are available [here](https://limmen.dev/csle/). 


## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020-2022, Kim Hammar

## See also

- [gym-idsgame](https://github.com/Limmen/gym-idsgame)
- [gym-optimal-intrusion-response](https://github.com/Limmen/gym-optimal-intrusion-response)
- [awesome-rl-for-cybersecurity](https://github.com/Limmen/awesome-rl-for-cybersecurity)

