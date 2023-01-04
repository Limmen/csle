---
title: What is CSLE?
permalink: /docs/what-is-csle/ 
---

## What is CSLE?

CSLE is a framework for evaluating and developing reinforcement learning agents for control problems in cyber security. 
Everything from network emulation, to simulation, and learning in CSLE have been co-designed to provide 
an environment where it is possible to train and evaluate reinforcement learning agents for practical 
cyber security tasks.

CSLE is an opinionated framework, which is based on a specific method for learning and evaluating security 
strategies for a given IT infrastructure (see Fig. 1). This method includes two systems: an emulation system and a 
simulation system.

<p align="center">
<img src="./../../img/arch.png" width="60%">
<p class="captionFig">
Figure 1: The method used to automatically find effective security strategies in CSLE.
</p>
</p>

The emulation system closely approximates the functionality of the target infrastructure and is used to run 
attack scenarios and defender responses. Such runs produce system measurements and logs, 
from which infrastructure statistics are estimated, which then are used to instantiate 
Markov decision processes (MDPs).

The simulation system is used to simulate the instantiated MDPs and to learn security strategies 
through reinforcement learning. Learned strategies are extracted from the simulation system and 
evaluated in the emulation system.

Three benefits of this method are: (*i*) 
that the emulation system provides a realistic environment to evaluate strategies; 
(*ii*) that the emulation system allows evaluating strategies without 
affecting operational workflows on the target infrastructure; 
and (*iii*}) that the simulation system enables efficient and rapid learning of strategies.
