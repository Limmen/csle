---
title: How-to Add Numerical Algorithms
permalink: /docs/how-to-numerical-algo/
---

## How-to: Add Numerical Algorithms
To add a new numerical algorithm called "`my_algorithm`" to the simulation system, 
perform the following steps:

1. Create a new sub-directory called `my_algorithm` inside the directory:
    ```bash
     csle/simulation-system/libs/csle-agents/src/csle_agents/agents/
    ```
   <p class="captionFig">
   Listing 177: Directory with numerical algorithms in CSLE.
   </p>
2. Implement the algorithm in a file called `my_algorithm.py` in the directory:
    ```bash
      csle/simulation-system/libs/csle-agents/src/csle_agents/agents/my_agent
    ```
   <p class="captionFig">
   Listing 178: Directory with algorithm implementation for the algorithm with the name `my_agent` in CSLE.
   </p>
   The implementation should be a Python class called `MyAlgorithm` that inherits from the class `BaseAgent`, 
   which is defined in the file:
   ```bash
    csle/simulation-system/libs/csle-agents/src/csle_agents/agents/base/base_agent.py
   ```
   <p class="captionFig">
   Listing 179: Base agent file in CSLE.
   </p>
3. Add an example of how to use the algorithm to the following folder:
    ```bash
     csle/examples
    ```
   <p class="captionFig">
   Listing 180: Directory with example usages of CSLE.
   </p>
