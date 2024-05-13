---
title: Operating CSLE
permalink: /docs/operating/
---

## Operating CSLE

This section describes commands and procedures that are useful when operating CSLE.
The framework can be operated in two ways,
either through the web interface or through the CLI (see Fig. 29).
This section focuses on the CLI, but more or less the same commands can be invoked through the web interface,
which should be self-explanatory.

<p align="center">
<img src="./../../img/csle_operation.png" width="70%">
<p class="captionFig">
Figure 29: User interfaces of CSLE; a user can execute commands to the management system 
through two interfaces: a web interface and a Command-Line Interface (CLI).
</p>
</p>

### Listing the Available Commands in the CLI
To list the available commands in the CSLE CLI, run the command:

```bash
csle help
```

<p class="captionFig">
Listing 102: Command to list the available commands in the CSLE CLI.
</p>

### Listing the State of CSLE
Information about the CSLE installation and its current state can be listed by executing the following command:

```bash
csle ls --all
```

<p class="captionFig">
Listing 103: Command to list the state of a CSLE installation.
</p>

### Starting, Stopping, and Resetting the Metastore

The metastore can be started by executing the following command:

```bash
sudo service postgresql start
```

<p class="captionFig">
Listing 104: Command to start the metastore.
</p>

The metastore can be stopped by executing the command:

```bash
sudo service postgresql stop
```

<p class="captionFig">
Listing 105: Command to stop the metastore.
</p>

To reset the metastore, execute the commands:

```bash
cd metastore; make clean
cd metastore; make build
```

<p class="captionFig">
Listing 106: Commands to reset the metastore. 
</p>

### Starting and Stopping the Management System

The management system can be started by executing the command:

```bash
csle start managementsystem
```

<p class="captionFig">
Listing 107: Command to start the management system.
</p>

The management system can be stopped by executing the command:

```bash
csle stop managementsystem
```

<p class="captionFig">
Listing 108: Command to stop the management system.
</p>

### Starting and Stopping Monitoring Systems

The monitoring systems Grafana, cAdvisor, Node exporter, and Prometheus can
be started by executing the commands:

```bash
csle start grafana
csle start cadvisor
csle start nodeexporter
csle start prometheus
```

<p class="captionFig">
Listing 109: Commands to start monitoring systems.
</p>

Similarly, Grafana, cAdvisor, Node exporter, and Prometheus can be stopped by executing the commands:

```bash
csle stop grafana
csle stop cadvisor
csle stop nodeexporter
csle stop prometheus
```

<p class="captionFig">
Listing 110: Commands to stop monitoring systems.
</p>

### Starting and Stopping Emulation Executions
To start an execution of an emulation configuration
with the name `csle-level9-010`, execute the following command:

```bash
csle start csle-level9-010
```

<p class="captionFig">
Listing 111: Command to start an execution of the emulation with configuration `csle-level9-010`.
</p>

Similarly, to stop an execution of an emulation configuration
with the name `csle-level9-010`, execute the following command:

```bash
csle stop csle-level9-010
```

<p class="captionFig">
Listing 112: Command to stop an execution of the emulation with configuration `csle-level9-010`.
</p>

The above command will stop all containers but will not remove them,
which means that the emulation can be started again with the same configuration
by running the command in Listing 111.

To stop an emulation execution and remove all of its containers and virtual networks, run the command:

```bash
csle clean csle-level9-010
```

<p class="captionFig">
Listing 113: Command to stop and clean an execution of the emulation with configuration `csle-level9-010`.
</p>

### Access a Terminal in an Emulated Container

To see which containers are running, execute the command:

```bash
csle ls --all
```

<p class="captionFig">
Listing 114: Command to list running CSLE containers.
</p>

To open a terminal in a running container,
e.g., a container with the name `mycontainer`, run the command:

```bash
csle shell mycontainer
```

<p class="captionFig">
Listing 115: Command to open a terminal in an emulated container. 
</p>