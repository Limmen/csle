# `gym-csle-stopping-game`

TODO

## Requirements

- Python 3.8+
- `csle-common`
- `csle-attacker`
- `csle-csle-defender`
- `csle-collector`
- 
## API documentation

This section contains instructions for generating API documentation using `sphinx`.

### Latest Documentation

The latest documentation is available at [https://limmen.dev/csle/docs/gym-csle-stopping-game](https://limmen.dev/csle/docs/gym-csle-stopping-game)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../gym_csle_stopping_game/
make html
```
To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle),
copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/gym-csle-stopping-game
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

(C) 2020-2022, Kim Hammar