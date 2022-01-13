# Emulation Environments

This directory contains scripts, configurations, and tools related to emulation environments of `csle`. Specifically:

- **Base images** ([base images](./base_images)): this directory contains base Docker images for emulating computer infrastructures.
- **Derived images** ([derived images](./derived_images)): this directory contains derived (from the base images) Docker images for emulating computer infrastructures.
- **Networks** ([networks](./networks)): this directory contains scripts for creating virtual subnetworks of Linux containers.
- **Management** ([management](./management)): this directory contains scripts and tools for managing emulated infrastructures (e.g. monitoring, starting, stopping, listing, etc.)
- **Use Cases** ([use_cases](./use_cases)): this directory contains scripts and tools for starting/stopping specific emulation configurations
- **Tests** ([tests](./tests)): this directory contains scripts and tools for starting/stopping test emulations

<p align="center">
<img src="docs/config_space.png" width="600">
</p>

## Installation

The emulations are built around Docker containers and virtual networking. 
A prerequisite is to have Docker installed:

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo groupadd docker
sudo usermod -aG docker $USER
```

See the latest documentation for installation here: 

- ([installation guide](https://docs.docker.com/engine/install/ubuntu/))
- ([post-installation guide](https://docs.docker.com/engine/install/linux-postinstall/))

It is recommended to enable swap limits in the kernel. To do that, follow these intructions:
1. Log into the Ubuntu or Debian host as a user with sudo privileges.
2. Edit the `/etc/default/grub` file. Add or edit the `GRUB_CMDLINE_LINUX` line to add the following two key-value pairs:
```bash
GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"
```
Save and close the file.
3. Update GRUB.
```bash
sudo update-grub
```
4. The changes take effect when the system is rebooted.

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../LICENSE.md)

Creative Commons

(C) 2020, Kim Hammar