---
title: Overall Architecture
permalink: /docs/overall-architecture/
---

## Overall Architecture

The overall architecture of CSLE is shown in the Fig. 2

<p align="center">
<img src="./../../img/overall_arch.png" width="60%">
<p class="captionFig">
Figure 2: Architecture of CSLE; it consists of an emulation system (bottom part), 
a management system (middle part), and a simulation system (upper part); 
the three systems are connected through APIs and a shared metastore.
</p>
</p>

In the middle of Fig. 2 is the management system, 
which orchestrates the overall execution of the framework and stores metadata in a 
distributed database called the metastore. It has three interfaces. 
One interface is a gRPC API to the emulation system, which emulates IT infrastructures 
using hardware and network virtualization. 
The other two interfaces—a web interface and a CLI—are to the simulation system, 
which simulates Markov decision processes and runs reinforcement learning workloads.

Users access CSLE in three ways: (1) through software functions using Python 
libraries of the simulation system; (2) through a web browser using the web interface; 
and (3) through a terminal using the CLI.