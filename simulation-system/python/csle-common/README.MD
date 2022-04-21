# `csle-common`

`csle-common` is a library with common functionality for all use-cases implemented in
CSLE. 

## Requirements

- Python 3.5+
- OpenAI Gym
- NumPy
- Pyglet (OpenGL 3D graphics)
- GPU for 3D graphics acceleration (optional)
- Torch (for baseline algorithms)
- Paramiko (for SSH tunnels)
- Docker (for interacting with the emulations)

## API Documentation 

This section contains instructions for generating API documentation using `sphinx`.

### Latest documentatation

TODO

### Generate API Documentation

```bash
cd docs
sphinx-apidoc -f -o source/ ../csle_common/
make html
```

## Installation & Tests

```bash
# install from pip
pip install csle-common==1.0.0
# local install from source
$ pip install -e csle-common
# force upgrade deps
$ pip install -e csle-common --upgrade

# git clone and install from source
git clone https://github.com/Limmen/csle
cd csle/simulation-system/gym-csle-stopping-game
pip3 install -e .
```

## Usage
The environment can be used as library of useful functionality when implementing 
use cases in csle.

```python
from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.running_emulation_env_config import RunningEmulationEnvConfig
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2021, Kim Hammar