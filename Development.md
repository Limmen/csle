# Developer Guide

## Install development tools

Install the `flake8` linter:
```bash
python -m pip install flake8
pip install -U pytest mock pytest-mock
```

Install ruby and its bundler to generate the documentation page:
```bash
sudo apt-get install ruby ruby-dev
sudo gem install bundler
```

Install Sphinx to automatically generate API documentation from docstrings: 
```bash
pip install sphinx sphinxcontrib-napoleon sphinx-rtd-theme
```

## Static code analysis

### Python: 
```bash
flake8 simulation-system/
flake8 csle-cli
flake8 emulation-system/envs
flake8 examples/
```

### JavaScript:
To run the linter and print possible errors, use the commands:
```bash
cd management-system/csle-mgmt-webapp/; npm run lint
```
To automatically fix linting errors, use the command:
```bash
cd management-system/csle-mgmt-webapp/; npm run lint:fix
```

## Generate API Documentation

To generate the Python API documentation, run:
```bash
simulation-system/python/generate_docs.sh
```

## Tests

### Unit tests

All unit tests must be written in a tests/ directory
File names should strictly start with tests_
Function names should strictly start with test

```bash
pytest tests/
pytest tests/test_sample.py
pytest tests/test_sample.py::test_function_one
```

### Integration tests


## Continuous Integration

## Lines of code

The project consists of aorund 120k lines of Python, 30k lines of JavaScript, 2.5k lines of Dockerfiles, 
1.4k lines of Makefile, and 1.6k lines of bash. 
The lines of code can be counted by executing the following commands from the project root:
``` bash
find . -name '*.py' | xargs wc -l
find . -name '*.js' | xargs wc -l
find . -name 'Dockerfile' | xargs wc -l
find . -name 'Makefile' | xargs wc -l
find . -name '*.sh' | xargs wc -l
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020-2022, Kim Hammar