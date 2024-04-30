---
title: How-to Add Base Containers
permalink: /docs/how-to-base-container/
---

## How-to: Add Base Containers
To add a base container with the name "`my_container`", do the following steps:

1. Create a sub-directory with the name `my_container` in the following directory:
   ```bash
     csle/emulation-system/base_images/docker_files
   ```
   <p class="captionFig">
   Listing 154: Directory with base Docker images.
   </p>
2. Add a Dockerfile to the following directory:
    ```bash
     csle/emulation-system/base_images/docker_files/my_container
    ```
   <p class="captionFig">
   Listing 155: Directory with the Dockerfile of a container with the name `my_container`.
   </p>
3. Add build and push instructions to the following Makefile:
    ```bash
      csle/emulation-system/base_images/Makefile
    ```
   <p class="captionFig">
   Listing 156: Makefile for base Docker images.
   </p>
4. Update the following README file:
     ```bash
     csle/emulation-system/base_images/README.md
     ```
   <p class="captionFig">
   Listing 157: README file for base Docker images.
   </p>
5. Build and push the image to DockerHub by running the commands:
    ```bash
     cd csle/emulation-system/base_images; make my_container
     cd csle/emulation-system/base_images; make push_my_container
    ```
   <p class="captionFig">
   Listing 158: Commands to build and push the base Docker image `my_container` to DockerHub.
   </p>
