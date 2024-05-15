---
title: How-to Add Configuration Parameters
permalink: /docs/how-to-config-param/
---

## How-to: Add Configuration Parameters
To add a new configuration parameter, perform the following steps:

1. Add the configuration parameter to the file: `csle/config.json`.
2. Add the new configuration parameter to the file:
    ```bash
     csle/simulation-system/libs/csle-common/src/csle_common/dao/emulation_config/config.py
    ```
   <p class="captionFig">
   Listing 181: Python file that manages the CSLE configuration.
   </p>
3. Add the new parameter to an appropriate class in the following file (add a new class if needed):
    ```bash
      csle/simulation-system/libs/csle-common/src/csle_common/constants/constants.py
    ```
   <p class="captionFig">
   Listing 182: Python file with constants in `csle-common`.
   </p>
