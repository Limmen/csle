---
title: Tests
permalink: /docs/tests/
---

## Tests

CSLE uses `pytest` for Python tests and integration tests, and `jest` for JavaScript tests.

The Python unit tests are available at:

- `csle/simulation-system/libs/csle-base/tests`
- `csle/simulation-system/libs/csle-agents/tests`
- `csle/simulation-system/libs/csle-attacker/tests`
- `csle/simulation-system/libs/csle-collector/tests`
- `csle/simulation-system/libs/csle-common/tests`
- `csle/simulation-system/libs/csle-defender/tests`
- `csle/simulation-system/libs/csle-rest-api/tests`
- `csle/simulation-system/libs/csle-ryu/tests`
- `csle/simulation-system/libs/csle-system-identification/tests`
- `csle/simulation-system/libs/gym-csle-stopping-game/tests`
- `csle/simulation-system/libs/csle-cluster/tests`
- `csle/simulation-system/libs/gym-csle-intrusion-response-game/tests`
- `csle/simulation-system/libs/gym-csle-apt-game/tests`
- `csle/simulation-system/libs/gym-csle-cyborg/tests`
- `csle/simulation-system/libs/csle-tolerance/tests`
- `csle/simulation-system/libs/csle-attack-profiler/tests`

To run the Python unit tests, execute the command:

```bash
simulation-system/libs/unit_tests.sh
```

<p class="captionFig">
Listing 135: Command to run the Python unit tests.
</p>

When adding new Python unit tests note that:

- All unit tests must be written in a `tests/` directory inside the Python project.
- File names should strictly start with "`tests_`".
- Function names should strictly start with "`test`".

The JavaScript unit tests are available at:

```bash
csle/management-system/csle-mgmt-webapp/src/
```

<p class="captionFig">
Listing 136: Directory with the JavaScript unit tests.
</p>

To run the JavaScript unit tests, execute the command:

```bash
cd management-system/csle-mgmt-webapp; npm test
```

<p class="captionFig">
Listing 137: Command to run the JavaScript unit tests.
</p>

To run the CSLE integration tests, execute the command:

```bash
simulation-system/libs/integration_tests.sh
```

<p class="captionFig">
Listing 138: Command to run the CSLE integration tests.
</p>
