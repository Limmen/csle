---
title: Installing Development Tools
permalink: /docs/installing-devtools/
---

## Installing Development Tools
This section contains instructions on how to install development tools that CSLE uses, 
such as test libraries and static code analyzers.

The Python build tool, which is used to package Python libraries, 
can be installed by running the command:

```bash
pip install -q build
```

<p class="captionFig">
Listing 88: Command to install the Python build tool.
</p>

The `twine` tool (a tool for publishing Python packages to PyPi) 
can be installed by running the command:

```bash
python3 -m pip install --upgrade twine
```

<p class="captionFig">
Listing 89: Command to install `twine`.
</p>

The `flake8` Python linter can be installed by running the command:

```bash
python -m pip install flake8
```

<p class="captionFig">
Listing 90: Command to install `flake8`.
</p>

The `mypy` static type checker for Python can be installed by running the command:

```bash
The `mypy` static type checker for Python can be installed by running the command:
```

<p class="captionFig">
Listing 91: Command to install `mypy`.
</p>

The `pytest` and `mock` test libraries for Python can be installed by running the command:

```bash
pip install -U pytest mock pytest-mock pytest-cov
```

<p class="captionFig">
Listing 92: Command to install `pytest` and `mock`.
</p>

Ruby and its bundler, which are used to generate the CSLE 
<a href="https://limmen.dev/csle/">documentation page </a>, can be installed by running the commands:

```bash
sudo apt-get install ruby ruby-dev
sudo gem install bundler
```

<p class="captionFig">
Listing 93: Commands to install Ruby and its bundler.
</p>

The `sphinx` Python library for automatic generation of API documentation 
can be installed by running the commands:

```bash
The `sphinx` Python library for automatic generation of API documentation can be installed by running the commands:
```

<p class="captionFig">
Listing 94: Commands to install `sphinx`.
</p>

Lastly, the `tox` Python library for automatic testing can be installed by running the command:

```bash
pip install tox
```

<p class="captionFig">
Listing 95: Command to install `tox`.
</p>

