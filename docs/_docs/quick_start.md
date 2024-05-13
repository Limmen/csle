---
title: Quick Start
permalink: /docs/quick-start/
---

## Quick Start

To verify that CSLE was installed correctly, run the command:

```bash
csle ls --all
```

<p class="captionFig">
Listing 97: Command to list all information about CSLE.
</p>

The above command lists information about the CSLE installation,
including the emulation configurations that are installed in the metastore.
Select one emulation configuration to start an execution, e.g., `csle-level9-010`,
and then run the command:

```bash
csle start csle-level9-010
```

<p class="captionFig">
Listing 98: Command to start an execution of the emulation configuration csle-level9-010.
</p>

The above command will start all containers of the emulation and apply the configuration.
After this process has completed, start the monitoring systems and the management
system by executing the commands:

```bash
csle start grafana
csle start cadvisor
csle start prometheus
csle start nodeexporter
csle start managementsystem
```

<p class="captionFig">
Listing 99: Command to start monitoring systems and the management system of CSLE.
</p>

After the above commands have completed, the web interface of CSLE can be accessed
at the URL: `http://localhost:7777/`, from which you can find links to Grafana's interface,
Prometheus interface, cAdvisor's interface, and interfaces to storage systems
(i.e., Kafka, Presto, and Elasticsearch).

To get started with reinforcement learning in CSLE, run the examples in the folder:
`csle/examples`, e.g.,

```bash
python csle/examples/training/ppo/
       stopping_pomdp_defender/run_vs_random_attacker_v_001.py
```

<p class="captionFig">
Listing 100: Command to run the Proximal Policy Optimization (PPO) algorithm for learning defender strategies in CSLE.
</p>