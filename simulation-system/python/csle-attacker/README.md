# `csle-attacker`

Scrips and programs for automating cyber attacks in CSLE. 
These attacks are used to evaluate defender policies and to collect data.


## Requirements

- Python 3.5+
- `csle-common`

## API documentation

This section contains instructions for generating API documentation using `sphinx`.

### Latest Documentation

The latest documentation is available at [https://limmen.dev/csle/docs/csle-attacker](https://limmen.dev/csle/docs/csle-attacker)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../csle_attacker/
make html
```
To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle), copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/csle-attacker
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2020-2022, Kim Hammar

