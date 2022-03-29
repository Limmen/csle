# `gym-csle-stopping-game`

TODO

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
- `csle-common` (library with common functionality for all csle environments)

## API Documentation 

This section contains instructions for generating API documentation using `sphinx`.

### Latest documentatation

TODO

### Generate API Documentation

```bash
cd docs
sphinx-apidoc -f -o source/ ../gym_csle_ctf/
make html
```

## Installation & Tests

```bash
# install from pip
pip install gym-csle-stopping-game==1.0.0
# local install from source
$ pip install -e gym-csle-stopping-game
# force upgrade deps
$ pip install -e gym-csle-stopping-game --upgrade

# git clone and install from source
git clone https://github.com/Limmen/csle
csle/simulation-system/gym-csle-stopping-game
pip3 install -e .
```

## Usage
The environment can be accessed like any other OpenAI environment with `gym.make`.
Once the environment has been created, the API functions
`step()`, `reset()`, `render()`, and `close()` can be used to train any RL algorithm of
your preference.

```python
TODO
```

## GUI

TODO 

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2022, Kim Hammar