# `csle-cli`

The command-line-interface (CLI) tool for CSLE. 

## Quickstart

To see the available commands, run:

```bash
csle --help
```

Examples:

- List available containers, emulations, images, and networks:

```bash
csle ls --all
```

- List containers only

```bash
csle ls containers --all
```

- List running containers only

```bash
csle ls containers
```

- List emulations

```bash
csle ls emulations --all
```

- List running emulations only

```bash
csle ls emulations
```

- Inspect a specific emulation/container/image/network

```bash
csle ls <name>
```

- Start/Stop/Clean a specific emulation/container

```bash
csle start| stop | clean <name>
```

- Open a shell in a given container

```bash
csle shell <container-name>
```

- Remove a container, image, network, emulation, or all

```bash
csle rm <container-name> | <network-name> | <image-name> | <emulation-name> all
```

- Install emulations, simulations, or Docker images

```bash
csle install emulations | simulations | derived_images | base_images | <emulation_name> | <simulation_name> | <derived_image_name> | <base_image_name> | metastore | all
```

- Uninstall emulations, simulations, or Docker images

```bash
csle uninstall emulations | simulations | derived_images | base_images | <emulation_name> | <simulation_name> | <derived_image_name> | <base_image_name> | metastore | all
```


## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2020-2022, Kim Hammar

