# `csle-agents`

A library with reinforcement learning algorithms, control-theoreitc algorithms, dynamic programming algorithms,
and game-theoretic algorithms for finding defender policies.

## Requirements

- Python 3.8+
- `csle-common`
- `csle-collector`
- `csle-attacker`
- `csle-defender`
- `csle-system-identification`
- `gym-csle-stopping-game`
- `pulp` (for linear and convex optimization)
- `Bayesian optimization` (for Bayesian optimization algorithms)

## API documentation

This section contains instructions for generating API documentation using `sphinx`.

### Latest Documentation

The latest documentation is available at [https://limmen.dev/csle/docs/csle-agents](https://limmen.dev/csle/docs/csle-agents)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../csle_agents/
make html
```
To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle), copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/csle-agents
```

### Static code analysis

```
flake8 .
```

### Unit tests

```
pytest
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2020-2022, Kim Hammar

