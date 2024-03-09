# Ansible installation

CSLE can be installed in two ways: (1) by manually executing the installation commands described in the documentation; and
(2) through Ansible. The recommended way to install CSLE is with Ansible as it automates repetitive tasks and simplifies management of the installation.
This folder contains configuration files and ansible playbooks for installing CSLE.

Ansible documentation can be found at [https://docs.ansible.com/](https://docs.ansible.com/).

## Installing Ansible

Ansible can be installed by running the command:
```bash
pip install ansible
```

## Configuring the installation
Before starting the CSLE installation, open the file XXX and configure the following variables:

- user
- todo

## Installing CSLE
To install CSLE with ansible, run the following commands:
```bash
ansible-playbook --ask-become-pass installing_the_management_system.yml
```

### Debugging
If the installation fails at some step, you can debug the reason for the failure by adding the following 
line to the Ansible playbook. First, we register a variable that holds a dictionary of the output for the module in that task. In the given example git_installation is this variable. In the next lines, we use debug to print the variable. 

```bash
- name: Installation of git
    apt:
      name: git
    register: git_installation
- debug:
    var: git_installation
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

Forough Shahab <foro@kth.se>

## Copyright and license

[LICENSE](../LICENSE.md)

Creative Commons

(C) 2020-2024, Kim Hammar
