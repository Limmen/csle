---
title: How-to Add Emulation Configurations
permalink: /docs/how-to-emulation-config/
---

## How-to: Add Emulation Configurations
To add a new emulation configuration with the name "`level_13`" and version 0.0.3, perform the following steps:

1. Create a sub-directory called `level_13` in the folder:
    ```bash
      csle/emulation-system/envs/003/
    ```
   <p class="captionFig">
   Listing 126: Directory with emulation configurations with version 0.0.3.
   </p>
2. Add the emulation configuration file `config.py` to the directory:
    ```bash
      csle/emulation-system/envs/003/level_13/
    ```
   <p class="captionFig">
   Listing 127: Directory with emulation configuration file for the emulation with the name `level_13` and version 0.0.3.
   </p>
3. Update the following README file:
    ```bash
      csle/emulation-system/envs/003/README.md
    ```
   <p class="captionFig">
   Listing 128: README file for emulation configurations with version 0.0.3.
   </p>
4. Update the following Makefile with installation instructions:
    ```bash
      csle/emulation-system/envs/003/README.md
    ```
   <p class="captionFig">
   Listing 129: Makefile for emulation configurations with version 0.0.3.
   </p>
5. Insert the emulation configuration into the metastore by running the command:
     ```bash
      csle/emulation-system/envs; make install
     ```
   <p class="captionFig">
   Listing 130: Command to insert emulation configurations into the metastore.
   </p>
