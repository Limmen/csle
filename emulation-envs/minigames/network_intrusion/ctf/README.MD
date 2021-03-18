# Capture the Flag

This folder contains a set of virtual environments for the `ctf` mini-game. 
A security game for autonomous agents where the goal of the attacker is to collect information about the system
and identify services with vulnerabilities, whereas the goal of the defender is to find and patch the vulnerabilities
as soon as possible and to detect the attacker.

There are several versions and difficulty levels of the minigame. Specifically:

- Version: **001**:
     - *Level 1* [./level_1](./level_1): A simple infrastructure with 6 nodes and weak-password-vulnerabilities
     - *Level 2* [./level_2](./level_2): A infrastructure with 12 nodes and weak-password-vulnerabilities
     - *Level 3* [./level_3](./level_3): A complex with 33 nodes and weak-password-vulnerabilities
     - *Level 4* [./level_4](./level_4): A simple infrastructure with 6 nodes and weak-password-vulnerabilities and IDS monitoring
     - *Level 5* [./level_5](./level_5): A infrastructure with 12 nodes and weak-password-vulnerabilities and IDS monitoring
     - *Level 6* [./level_6](./level_6): A complex with 33 nodes and weak-password-vulnerabilities and IDS monitoring
     - *Level 7* [./level_7](./level_7): A infrastructure with 14 nodes and several vulnerabilities: SambaCry, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1,and SQL injection., as well as SSH, FTP, Telnet servers that can be compromised using dictionary attacks
     - *Random* [./random](./random): Generates a random infrastructure with a specified number of nodes and vulnerabilities
     - *Many Random* [./random_many](./random_many): Generates several random infrastructures with specified number of nodes and vulnerabilities                          
    
  
## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020, Kim Hammar