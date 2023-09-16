---
title: Why CSLE?
permalink: /docs/why-csle/
---

## Why is CSLE?

As the ubiquity and evolving nature of cyber attacks is of growing concern to society, 
*automation* of security processes and functions has been recognized as an important 
part of the response to this threat. A promising approach to achieve this automation is 
*reinforcement learning*, which has proven effective in finding near-optimal solutions 
to control problems in several domains 
(e.g., robotics and industry automation), and is actively investigated as an approach 
to automated security (see <a href="https://github.com/Limmen/awesome-rl-for-cybersecurity">survey</a>). 
While encouraging results have been obtained in this line of research, key challenges remain. 
Chief among them is narrowing the gap between the environment where the reinforcement learning agents 
are evaluated and a scenario playing out in a real system. Most of the results obtained so far 
are limited to simulation environments, and it is not clear how they generalize to 
practical IT infrastructures. Another limitation of prior research is the lack of 
common benchmarks and toolsets.

CSLE was developed to address precisely the above limitations. By using high-fidelity emulations, 
it narrows the gap between the evaluation environment and a real system, 
and by being open-source, it provides a foundation for further research to build on.

Recently, efforts to build similar frameworks as CSLE has started (see
<a href="https://github.com/Limmen/awesome-rl-for-cybersecurity">survey</a>). Most notably, there is
<a href="https://github.com/microsoft/CyberBattleSim">CyberBattleSim</a> by Microsoft,
<a href="https://github.com/cage-challenge/CybORG">CyBorg</a> by
the Australian department of defence, <a href="https://github.com/dstl/YAWNING-TITAN">Yawning Titan</a> by
the UK Defence Science and Technology Laboratory (DSTL), <a href="https://arxiv.org/abs/2109.03331">CyGIL</a> by
Defence Research and Development Canada (DRDC), <a href="https://arxiv.org/pdf/2305.17246.pdf">NASimEmu</a>
by the Czech Technical University in Prague and <a href="https://arxiv.org/pdf/2103.07583.pdf">FARLAND</a>
, which is developed at USA's National Security Agency (NSA). Some of these frameworks only include
simulation components and some of them include both simulation and emulation components.

In contrast to these frameworks, CSLE is fully open-source, 
includes both a simulation component and an emulation component,
and has demonstrated the capabilitiy to learn near-optimal defender strategies on specific use cases 
(see <a href="publications">publications</a>).

  




