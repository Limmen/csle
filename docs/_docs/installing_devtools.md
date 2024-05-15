---
title: Installing Development Tools
permalink: /docs/installing-devtools/
---

## Installing Development Tools
This section contains instructions on how to install development tools that CSLE uses, 
such as test libraries and static code analyzers.

To install all Python build tools at once, run the following commands:

```bash
csle/simulation-system/libs/csle-base; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-collector; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-ryu; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-common; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-attacker; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-defender; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-system-identification; pip install -r requirements_dev.txt
csle/simulation-system/libs/gym-csle-stopping-game; pip install -r requirements_dev.txt
csle/simulation-system/libs/gym-csle-apt-game; pip install -r requirements_dev.txt
csle/simulation-system/libs/gym-csle-cyborg; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-agents; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-rest-api; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-cli; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-cluster; pip install -r requirements_dev.txt
csle/simulation-system/libs/gym-csle-intrusion-response-game; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-tolerance; pip install -r requirements_dev.txt
csle/simulation-system/libs/csle-attack-profiler; pip install -r requirements_dev.txt 
```

<p class="captionFig">
Listing 124: Command to install the Python build tool.
</p>
It is also possible to install all development tools at once by running the script `simulation-system/libs/local_install_dev.sh`

Alternatively, install each development library separately by following the commands below.

The Python build tool, which is used to package Python libraries, 
can be installed by running the command:

```bash
pip install -q build
```

<p class="captionFig">
Listing 125: Command to install the Python build tool.
</p>

The `twine` tool (a tool for publishing Python packages to PyPi) 
can be installed by running the command:

```bash
python3 -m pip install --upgrade twine
```

<p class="captionFig">
Listing 126: Command to install `twine`.
</p>

The `flake8` Python linter can be installed by running the command:

```bash
python -m pip install flake8
```

<p class="captionFig">
Listing 127: Command to install `flake8`.
</p>

The `mypy` static type checker and associated type libraries for Python can be installed by running the command:

```bash
python3 -m pip install -U mypy mypy-extensions mypy-protobuf types-PyYAML types-protobuf types-paramiko types-requests types-urllib3
```

<p class="captionFig">
Listing 128: Command to install `mypy`.
</p>

The `pytest` and associated test libraries for Python can be installed by running the command:

```bash
pip install -U pytest mock pytest-mock pytest-cov pytest-grpc
```

<p class="captionFig">
Listing 129: Command to install `pytest` and `mock`.
</p>

Ruby and its bundler, which are used to generate the CSLE 
<a href="https://limmen.dev/csle/">documentation page </a>, can be installed by running the commands:

```bash
sudo apt-get install ruby ruby-dev
sudo gem install bundler
```

<p class="captionFig">
Listing 130: Commands to install Ruby and its bundler.
</p>

The `sphinx` Python library for automatic generation of API documentation 
can be installed by running the commands:

```bash
The `sphinx` Python library for automatic generation of API documentation can be installed by running the commands:
```

<p class="captionFig">
Listing 131: Commands to install `sphinx`.
</p>

Lastly, the `tox` Python library for automatic testing can be installed by running the command:

```bash
pip install tox
```

<p class="captionFig">
Listing 132: Command to install `tox`.
</p>

