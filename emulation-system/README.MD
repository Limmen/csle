# Emulation Environments

This directory contains scripts, configurations, and tools related to emulation environments of `csle`. Specifically:

- **Base images** ([base images](./base_images)): this directory contains base Docker images for emulating computer infrastructures.
- **Derived images** ([derived images](./derived_images)): this directory contains derived (from the base images) Docker images for emulating computer infrastructures.
- **Environments** ([envs](./envs)): this directory contains pre-configured emulation environments

<p align="center">
<img src="docs/config_space.png" width="600">
</p>

## Installation
To install all images and emulations, run:
```bash
make build
```

To remove all images and all emulations, run: 
```bash
make rm
```

For more detailed information about installation of images, see ([README](./base_images/README.MD)), 
([README](./derived_images/README.MD)) and ([README](./envs/README.md)),

### Install and setup Docker

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

### Setup maximum file descriptors
If have a large server and pĺan on running several emulations in paralell, it is recommended to to increase 
the limit on the number of open file descriptors since the Kafka cluster for each emulation will use quite 
a lot of desciptors. To do this, follow the steps below:
```
ulimit -Sn # check the soft limit
ulimit -Hn # check the hard limit
sudo emacs -nw /etc/security/limits.conf # open the limits conf file

# (Example) add the lines:
kim             soft       nofile          102400
kim             hard       nofile          1024000
```

### Install Open vSwitch (OVS)  for SDN emulations
```bash
sudo apt install -y openvswitch-switch
```

### Install Emulation System

TODO

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../LICENSE.md)

Creative Commons

(C) 2020-2022, Kim Hammar