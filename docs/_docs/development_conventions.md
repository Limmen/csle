---
title: Development Conventions
permalink: /docs/development-conventions/
---

## Development Conventions

Being a project of certain size and complexity,
it is important that the general development conventions of CSLE are followed.
By adopting good practices it will be easier to deal with the growth of this project.

Please note that if you decide to contribute to CSLE you automatically
accept the licensing conditions of this project (CC BY-SA 4.0 license).

### General Principles

CSLE tries to follow a few high-level principles in making both technical and community decisions,
which are listed below.
They are goals to shoot for, and may not be followed perfectly all the time.

- **Code over configuration.** We aim to make CSLE fully programmable, everything from starting/stopping emulations to configuring a service running on a container should be possible through a program function. To achieve this level of programmability, as much as possible of CSLE should be defined in code rather than configuration files. If a configuration file is necessary, it should be defined in a serialization format that easily can be converted back to code, e.g., a JSON file that maps to a Python class. Another benefit of defining configuration in code is that we can run the configuration through the code quality toolchain to identify bugs and style errors.

- **Separation of concerns.** CSLE is divided into components (systems), e.g., the management system, the emulation system, and the simulation system. These components interact via APIs and via a shared database (the metastore). As much as possible, each individual component should be independent of the other components. This principle allows users to install individual components without having to install the other components.

- **Release early and often.** We should emphasize smaller, more iterative releases over large and complex ones. This keeps our documentation in-line with the latest releases and also minimizes the disruption (and subsequent maintenance burden) associated with big changes. The process for creating a release is relatively simple and quick, so don't hesitate to release patch versions (or minor versions) as appropriate.


### Structure of CSLE

CSLE is made up of numerous libraries and artifacts in different programming languages (mainly Python,
JavaScript, Bash, and Dockerfiles). When you initially consider contributing to CSLE,
you might be unsure about which of those libraries implement
the functionality you want to change or report a bug for.
The list below, which explains the main components of CSLE and their location in the code repository,
should help you with that.

- `examples/`. Examples of using CSLE.
- `emulation-system/base_images` and `emulation-system/derived_images`. Dockerfiles that define the container images of the emulation system.
- `emulation-system/envs`. Emulation configurations.
- `metastore`. SQL files that define the data model of the metastore.
- `management-system/csle-mgmt-webapp`. Web application that implements the web interface of CSLE.
- `simulation-system/envs`. Simulation configurations.
- `simulation-system/libs/csle-base`. A Python library with definitions and base classes for the other Python libraries in CSLE.
- `simulation-system/libs/csle-agents`. A Python library with implementations of control, learning, and game-theoretic algorithms for finding defender strategies.
- `simulation-system/libs/csle-attacker`. A Python library that contains code for emulating attacker actions.
- `simulation-system/libs/csle-cli`. A Python library with the CSLE CLI.
- `simulation-system/libs/csle-collector`. A Python library that implements the monitoring and management agents.
- `simulation-system/libs/csle-common`. A Python library that contains common functionality to all CSLE Python libraries.
- `simulation-system/libs/csle-defender`. A Python library that contains code for emulating defender actions.
- `simulation-system/libs/csle-cluster`. A Python library that contains a gRPC server for cluster management in CSLE.
- `simulation-system/libs/csle-rest-api`. A Python library with the CSLE REST API.
- `simulation-system/libs/csle-ryu`. A Python library with RYU SDN controllers.
- `simulation-system/libs/csle-system-identification`. A Python library with implementations of system identification algorithms to learn system models based on measured data and traces.
- `simulation-system/libs/gym-csle-stopping-game`. A gym environment for an optimal stopping game.
- `simulation-system/libs/gym-csle-intrusion-response-game`. A gym environment for an intrusion response game.
- `simulation-system/libs/csle-tolerance`. An intrusion-tolerant system: Tolerance: (T)w(o)-(l)ev(e)l (r)ecovery (a)nd respo(n)se (c)ontrol with f(e)edback.
- `simulation-system/libs/gym-csle-apt-game`. A gym environment for an APT game.
- `simulation-system/libs/gym-csle-cyborg`. A gym environment wrapper for CybORG.
- `simulation-system/libs/csle-attack-profiler`. An attack profiler based on MITRE ATT&CK

#### Code Readability

The code style in CSLE is based on [PEP 8](https://peps.python.org/pep-0008/) defined using the `flake8` Python linter and the `eslint` JavaScript linter. You can configure your IDE or editor to automatically enforce these guidelines.

The configuration file of the Python linter is located at:

```bash
csle/.flake8
```

<p class="captionFig">
Listing 120: Configuration file for the `flake8` Python linter.
</p>

Configuration file for the `flake8` Python linter.

```bash
csle/management-system/csle-mgmt-webapp/.eslintrc.json
```

<p class="captionFig">
Listing 121: Configuration file for the `eslint` JavaScript linter.
</p>


Names of variable, functions, methods etc. should be clear and descriptive, not cryptic.
All Python functions and variables should be written in `snake_case`,
e.g., `stop_all_executions()`. All JavaScript functions and variables should be
in `CamelCase`, e.g., `getAgentType()`.

It is common practice to name simple loop variables i, j, and k, so there's no
need to give them silly names like `the_index` unless it's necessary for some reason or other.

Avoid long lines (>120 characters) if possible. This principle makes pull requests smaller,
makes the code more readable, and benefits co-developers editing code in
Emacs/Vim over SSH and/or in narrower windows.

It is highly recommended that you configure your editor or Integrated Development Environment (IDE) to automatically enforce the style guidelines.

### Comments in Code
All functions and classes should have comments that document the input/output arguments,
the purpose of the function/class, and its return value.
These comments are used to automatically generate API documentation.

Example of a comment to a Python function:

```python
@staticmethod
def stop_all_executions() -> None:
    """
    Stops all emulation executions

    :return: None
    """
    executions = MetastoreFacade.list_emulation_executions()
    for exec in executions:
        EmulationEnvController.stop_containers(execution=exec)
        ContainerController.stop_docker_stats_thread(
                          execution=exec)
```

<p class="captionFig">
Listing 122: Example of a Python function with a comment.`
</p>

Example of a comment to a JavaScript function:

```javascript
const convertListToCommaSeparatedString = (listToConvert) => {
    /**
     * Converts a list of strings into a single comma-separated
     * string
     *
     * @param listToConvert the list to convert
     * @returns {string` the comma separated string
     */
    var str = ""
    for (let i = 0; i < listToConvert.length; i++) {
        if (i !== listToConvert.length-1) {
            str = str + listToConvert[i] + ", "
        ` else {
            str = str + listToConvert[i]
        `
    `
    return str
`
```

<p class="captionFig">
Listing 123: Example of a JavaScript function with a comment.
</p>

### Unit and Integration Testing
Every new change to the code must pass the tests (tests are performed automatically on each pull request).
Whenever a new feature is added to CSLE, a corresponding test should be added
(see <a href="../tests">this page</a> for instructions on how to add tests).

### How We Use Git

We use the Git-Flow branching model, in which branches are categorized into:

- A master branch.
- A main development branch.
- One or several feature branches.
- One or several hotfix branches.

The code on the main branch (often called `main` or `release`) is stable,
properly tested and is the version of the code that a typical user should pick.
No changes are made directly on the master branch.

The code on the development branch (often called `develop`)
should be working, but without guarantees. For small features,
development might well happen directly on the development branch
and the code here may therefore sometimes be broken (this should ideally never happen though).
When the development branch is deemed "done" and has undergone testing and review,
it is merged into the master branch. The release is then tagged with an appropriate release version.

A feature branch (often called `feature/some_name` where `some_name`
is a very short descriptive name of the feature) is branched off
from the main development branch when a new "feature" is being implemented.
A new feature is any logically connected set of changes to the code
base regardless of how many files are being changed.

A hotfix branch (often called `hotfix/some_name`) is a branch that implements
a bugfix to a release. In terms of branching, it is thus very similar
to a feature branch but for the master branch rather than for the development branch.
A hotfix should fix critical errors that were not caught in testing
before the release was made. Hotfixes should not implement new behavior,
unless this is needed to fix a critical bug. Hotfixes need to undergo
review before they are merged back into the master and development branches.

The master and development branches are never deleted,
while the others are transient (temporary, for the duration of the development and code review).

The benefits of this type of branching model in development are:

- Co-developers work on separate branches, and do not "step on each other's toes" during the development process, even if they push their work back to GitHub.
- Co-developers and users have a stable master branch to use.
- Features in "feature" branches are independent of each other. Any conflicts are resolved when merging.

Commit often, possibly several times a day. It's easier to roll back a small commit than
to roll back large commits. This practice also makes the code easier to review.
Remember to push the commits to GitHub every once in a while too.
Write a helpful commit message with each commit that describes
what the changes are and possibly even why they were necessary.

### Continuous Integration

We use continuous integration (CI) with GitHub Actions to build the project
and run tests on every pull request submitted to CSLE.
The CI pipeline used in CSLE is illustrated in Fig. 30.
Developers make commits on a branch that is separated from the master/main branch.
Once a developer has completed a bugfix or a new feature, he/she submits a pull request to GitHub.
The pull request then triggers a set of automated tests and automated builds using GitHub actions.
If all automated tests pass, the pull request undergoes code review,
otherwise the developer has to fix the failing tests or builds.
Finally, when the code review and associated fixes are completed,
the pull request is merged into the main/master branch and
may optionally trigger a release pipeline where build artifacts are pushed
to code servers (i.e., DockerHub and PyPi).

<p align="center">
<img src="./../../img/ci_pipeline.png" width="75%">
<p class="captionFig">
Figure 30: The continuous integration (CI) pipeline of CSLE.
</p>
</p>

### Bug Reports

Please be aware of the following things when filing bug reports:

1. Avoid raising duplicate issues. Use the GitHub issue search feature to check whether your bug report or feature request has been mentioned in the past. Duplicate bug reports and feature requests are a huge maintenance burden on the limited resources of CSLE. If it is clear from your report that you would have struggled to find the original issue, that's ok, but if searching for a selection of words in your issue title would have found the original issue, then the duplicate issue will likely be closed abruptly.

2. When filing bug reports about exceptions or tracebacks, please include the complete traceback. Partial tracebacks, or just the exception text, are not helpful. Issues that do not contain complete tracebacks may be closed without warning.

3. Make sure you provide a suitable amount of information to work with. This means that you should provide:
    - Guidance on how to reproduce the issue. Ideally, this should be a small code sample that can be run immediately by the maintainers. Failing that, let us know what you're doing, how often it happens, what environment you're using, etc. Be thorough: it prevents us needing to ask further questions.
    - Tell us what you expected to happen. When we run your example code, what are we expecting to happen? What does "success" look like for your code?
    - Tell us what actually happens. It's not helpful for you to say "it doesn't work" or "it fails". Tell us how it fails: do you get an exception? A hang? A non-200 status code? How was the actual result different from your expected result?
   If you do not provide all of these things, it will take us much longer to fix your problem. If we ask you to clarify these things and you never respond, we will close your issue without fixing it.

### Contribution Flow
Our contribution flow is very straightforward and follows an issue-pull request workflow.
Contributors need to fork the repository for having their contributions landed on the project.
If you are looking to contribute, we have laid down a series of steps that we would like you to follow.

1. **Find an issue to work on.** The first step is to go through the issues to find one that you would like to contribute to (or possibly open a new issue). Exploring the issues and pull requests will give you an idea of how the contribution flow works. Upon finding something to work on, you can either request for the issue to be assigned to you (if someone else has created the Issue) or you can make your own. To ensure that the issue is received positively by the maintainers, make sure of the following:
   - If you are filing a bug report, make sure that the report follows the guidelines stated above.
   - If you are filing a feature request, make sure that you pitch in your idea well and in a constructive manner.
2. **Getting your pull request merged.** To make sure you land a great contribution, we would request you to follow the standard Git & GitHub workflow for code collaboration. We would recommend:
   - Every pull request should have the corresponding issue linked to it.
   - Every pull request should pass the automated CI checks.
   - Every pull request should be as atomic as possible.
   - Every pull request should include a test verifying the new/fixed behavior.
3. **Reviewing pull requests.** After landing your pull request, the maintainers will review it and provide actionable feedback. Maintainers expect the comments to be resolved once a review has been completed. You can provide updates if you are still working on it to help us understand the areas where we can help.
