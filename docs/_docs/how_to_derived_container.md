---
title: How-to Add Derived Containers
permalink: /docs/how-to-derived-container/
---

## How-to: Add Derived Containers
To add a derived container with the name "`my_container`", perform the following steps:

1. To add a derived container with the name "`my_container`", perform the following steps:
    ```bash
     csle/emulation-system/derived_images/
    ```
   <p class="captionFig">
   Listing 159: Directory with derived Docker images.
   </p>
2. Add a Dockerfile inside the directory:
    ```bash
     csle/emulation-system/derived_images/my_container/
    ```
   <p class="captionFig">
   Listing 160: Directory with the Dockerfile for a derived Docker image with the name `my_container`.
   </p>
3. Add build and push instructions to the following Makefile:
    ```bash
     csle/emulation-system/derived_images/Makefile
    ```
   <p class="captionFig">
   Listing 161: Makefile for derived Docker images.
   </p>
4. Update the following README file:
    ```bash
     csle/emulation-system/derived_images/README.md
    ```
   <p class="captionFig">
   Listing 162: README file for derived Docker images.
   </p>
5. Build and push the image to DockerHub by running the commands:
    ```bash
     cd csle/emulation-system/derived_images; make my_container
     cd csle/emulation-system/derived_images; make push_my_container
    ```
   <p class="captionFig">
   Listing 163: Commands to build and push the derived Docker image `my_container` to DockerHub.
   </p>
