# `csle-ryu`

A library with SDN controllers used in CSLE for emulating software-defined networks.

## Requirements

- Python 3.5+
- `ryu` (for HTTP server)
- `eventlet` (for HTTP server)
- `confluent-kafka` (for interacting with Kafka)
- `sphinx` (for API documentation)
- `sphinxcontrib-napoleon` (for API documentation)
- `sphinx-rtd-theme` (for API documentation)

## API documentation

This section contains instructions for generating API documentation using `sphinx`.

### Latest Documentation

The latest documentation is available at [https://limmen.dev/csle/docs/csle-ryu](https://limmen.dev/csle/docs/csle-ryu)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../csle_ryu/
make html
```
To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle), 
copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/csle-ryu
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2020-2022, Kim Hammar

