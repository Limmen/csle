# `pycr-common`

`pycr-common` is a library with common functionality for all use-cases implemented in
pycr. 

## Requirements

- Python 3.5+
- OpenAI Gym
- NumPy
- Pyglet (OpenGL 3D graphics)
- GPU for 3D graphics acceleration (optional)
- Jsonpickle (for configuration files)
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
sphinx-apidoc -f -o source/ ../pycr_common/
make html
```

## Installation & Tests

```bash
# install from pip
pip install pycr-common==1.0.0
# local install from source
$ pip install -e pycr-common
# force upgrade deps
$ pip install -e pycr-common --upgrade

# git clone and install from source
git clone https://github.com/Limmen/pycr
cd pycr/python-envs/use_cases/intrusion_prevention/minigames/ctf/gym-pycr-ctf
pip3 install -e .
```

## Usage
The environment can be used as library of useful functionality when implementing 
use cases in pycr.

```python
from pycr_common.dao.network.env_mode import EnvMode
from pycr_common.dao.network.emulation_config import EmulationConfig
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../../../LICENSE.md)

(C) 2021, Kim Hammar