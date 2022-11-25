# `csle-system-identification`

A library with system identification algorithms for learning system models in CSLE based on traces and data collected
from emulated infrastructures.

## Requirements

- Python 3.8+
- `csle-common`
- `csle-collector`
- `csle-attacker`
- `csle-defender`
- `gpytorch` (For system identification algorithms based on Gaussian processes)

## API documentation

This section contains instructions for generating API documentation using `sphinx`.

### Latest Documentation

The latest documentation is available at [https://limmen.dev/csle/docs/csle-system-identification](https://limmen.dev/csle/docs/csle-system-identification)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../csle_system_identification/
make html
```
To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle),
copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/csle-system-identification
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2020-2022, Kim Hammar

