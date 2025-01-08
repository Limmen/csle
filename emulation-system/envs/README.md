# Emulation environments

This folder contains emulation environments.

- Version: **060** [./060](060):
  - *Level 1* [level_1](060/level_1): A simple infrastructure with 6 nodes and weak-password-vulnerabilities
  - *Level 2* [level_2](060/level_2): An infrastructure with 12 nodes and weak-password-vulnerabilities
  - *Level 3* [level_3](060/level_3): A complex infrastructure with 33 nodes and weak-password-vulnerabilities
  - *Level 4* [level_4](060/level_4): A simple infrastructure with 6 nodes and weak-password-vulnerabilities and IDS monitoring
  - *Level 5* [level_5](060/level_5): An infrastructure with 12 nodes and weak-password-vulnerabilities and IDS monitoring
  - *Level 6* [level_6](060/level_6): A complex infrastructure with 33 nodes and weak-password-vulnerabilities and IDS monitoring
  - *Level 7* [level_7](060/level_7): An infrastructure with 15 nodes and several vulnerabilities: SambaCry, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1,and SQL injection., as well as SSH, FTP, Telnet servers that can be compromised using dictionary attacks
  - *Level 8* [level_8](060/level_8): An infrastructure with 26 nodes and several vulnerabilities: SambaCry, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1,and SQL injection., as well as SSH, FTP, Telnet servers that can be compromised using dictionary attacks
  - *Level 9* [./level_9](060/level_9): A complex infrastructure with 36 nodes and and several vulnerabilities: SambaCry, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1, SQL injection, and brute-force vulnerabilities. Further, the infrastructure has IDS monitoring
  - *Level 10* [./level_10](060/level_10): An infrastructure with 16 nodes and several vulnerabilities: SambaCry, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1,and SQL injection., Pengine Server RCE Exploit, as well as SSH, FTP, Telnet servers that can be compromised using dictionary attacks
  - *Level 11* [./level_11](060/level_11): A complex infrastructure with 36 nodes and and several vulnerabilities: SambaCry, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1, SQL injection, and brute-force vulnerabilities. Further, the infrastructure has IDS monitoring
  - *Level 12* [./level_12](060/level_12): A simple software-defined networking environment
  - *Level 13* [./level_13](060/level_13): A complex infrastructure with 64 nodes and several vulnerabilities: SambaCry, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1,and SQL injection., Pengine Server RCE Exploit, as well as SSH, FTP, Telnet servers that can be compromised using dictionary attacks
  - *Level 14* [./level_14](060/level_14): An infrastructure with a flat topology and 17 nodes and several vulnerabilities: SambaCry, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1,and SQL injection., Pengine Server RCE Exploit, as well as SSH, FTP, Telnet servers that can be compromised using dictionary attacks
  - *Level 15* [./level_15](060/level_15): A infrastructure with 4 nodes and weak-password vulnerabilities.

## Useful commands:

- Install all emulations:
  ```bash
  make install
   ```

- Uninstall all emulations:
  ```bash
  make uninstall
   ```

- Clean the configuration of all emulations:
  ```bash
  make clean_config
   ```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../LICENSE.md)

Creative Commons

(C) 2020-2025, Kim Hammar