# Emulation environments

This folder contains emulation environments. 

- **Capture the flag ([ctf](./network_intrusion/ctf))** 
  Several CTF's with varying difficulty are implemented, see:
     - [level_1](./network_intrusion/ctf/001/level_1)
     - [level_2](./network_intrusion/ctf/001/level_2)
     - [level_3](./network_intrusion/ctf/001/level_3)
     - [level_4](./network_intrusion/ctf/001/level_4)
     - [level_5](./network_intrusion/ctf/001/level_5)
     - [level_6](./network_intrusion/ctf/001/level_6)
     - [level_7](./network_intrusion/ctf/001/level_7)

## Useful commands:

- Install all emulations:
  ```bash
  make install
   ```

- Uninstall all emulations:
  ```bash
  make uninstall
   ```

- Clean all emulations:
  ```bash
  make clean
   ```

- Stop all emulations:
  ```bash
  make stop
   ```

- Run all emulations (Warning: don't do this on a machine with limited resources):
  ```bash
  make run
   ```

- Clean the configuration of all emulations:
  ```bash
  make clean_config
   ```

- Apply the configuration of all emulations:
  ```bash
  make apply_config
   ```