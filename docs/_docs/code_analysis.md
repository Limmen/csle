---
title: Static Code Analysis
permalink: /docs/code-analysis/
---

## Static Code Analysis

Static code analyzers are used in CSLE to enforce style guidelines and discover bugs. 
The `flake8` linter and the `mypy` type checker 
are used to analyze the Python code and the `eslint` 
linter is used to analyze the JavaScript code.

To run the Python linter on the CSLE code base, execute the command:

```bash
./python_linter.sh
```

<p class="captionFig">
Listing 139: Command to run the Python linter.
</p>

Alternatively, the following commands can be executed for the same effect as the command above:

```bash
flake8 simulation-system/
flake8 csle-cli
flake8 emulation-system/envs
flake8 examples/
```

<p class="captionFig">
Listing 140: Commands to run the Python linter.
</p>

To run the Python static type checker, execute the command:

```bash
simulation-system/libs/type_checker.sh
```

<p class="captionFig">
Listing 141: Command to run the Python static type checker.
</p>

To run the JavaScript linter, run the commands:

```bash
cd management-system/csle-mgmt-webapp/; npm run lint
cd management-system/csle-mgmt-webapp/; npm run lint:fix
```

<p class="captionFig">
Listing 142: Commands to run the JavaScript linter.
</p>
