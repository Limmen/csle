---
title: How-to Add Simulation Configurations
permalink: /docs/how-to-simulation-config/
---

## How-to: Add Simulation Configurations
To add a new simulation environment with the name "`test_env`" and version 0.0.1, 
perform the following steps:

1. Create a sub-directory called `test_env` in the folder:
     ```bash
       csle/simulation-system/envs/
     ```
   <p class="captionFig">
   Listing 169: Directory with simulation configurations.
   </p>
2. Add the simulation configuration file `config_v_001.py` to the directory:
     ```bash
       1 csle/simulation-system/envs/test_env
     ```
   <p class="captionFig">
   Listing 170: Directory with configuration file for the simulation environment with the name `test_env`.
   </p>
3. Update the following README file:
    ```bash
      csle/simulation-system/envs/README.md
    ```
   <p class="captionFig">
   Listing 171:
   </p>
4. Update the following Makefile with installation instructions:
    ```bash
      csle/simulation-system/envs/Makefile
    ```
   <p class="captionFig">
   Listing 172: Makefile for simulation configurations.
   </p>
5. Insert the simulation configuration into the metastore by running the command:
     ```bash
       csle/simulation-system/envs; make install
     ```
   <p class="captionFig">
   Listing 173: Command to insert simulation configurations into the metastore.
   </p>

