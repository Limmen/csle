---
title: Resources
permalink: /docs/resources/
---

## Resources

Resources for getting started with CSLE are described below.

### Documentation
Apart from the web documentation (i.e., the documentation you are reading now), which is available at
<a href="https://limmen.dev/csle/">https://limmen.dev/csle/</a>, there are official release documents, 
which are available in PDF format for each release <a href="https://github.com/Limmen/csle/tree/master/releases">here</a>. 
Video demonstrations of earlier versions of CSLE are available on YouTube: 

- <a href="https://www.youtube.com/watch?v=18P7MjPKNDg&t=1s">Demonstration of v0.0.1</a>
- <a href="https://www.youtube.com/watch?v=iE2KPmtIs2A&">Demonstration of v0.2.0</a>
- <a href="https://www.youtube.com/watch?v=l_g3sRJwwhc">Demonstration of the installation of v0.5.0</a>

### Source code, Binaries, and Docker Images

The source code of CSLE is available on GitHub:
<a href="https://github.com/Limmen/csle">https://github.com/Limmen/csle</a> and the Docker images are 
available on DockerHub:
<a href="https://hub.docker.com/u/kimham">https://hub.docker.com/u/kimham</a>. 
Further, binaries of the Python libraries in CSLE are available on PyPi:

- <a href="https://pypi.org/project/csle-base">https://pypi.org/project/csle-base</a>
- <a href="https://pypi.org/project/csle-collector">https://pypi.org/project/csle-collector</a>
- <a href="https://pypi.org/project/csle-common">https://pypi.org/project/csle-common</a>
- <a href="https://pypi.org/project/csle-attacker">https://pypi.org/project/csle-attacker</a>
- <a href="https://pypi.org/project/csle-defender">https://pypi.org/project/csle-defender</a>
- <a href="https://pypi.org/project/gym-csle-stopping-game">https://pypi.org/project/gym-csle-stopping-game</a>
- <a href="https://pypi.org/project/gym-csle-apt-game">https://pypi.org/project/gym-csle-apt-game</a>
- <a href="https://pypi.org/project/gym-csle-cyborg">https://pypi.org/project/gym-csle-cyborg</a>
- <a href="https://pypi.org/project/csle-ryu">https://pypi.org/project/csle-ryu</a>
- <a href="https://pypi.org/project/csle-rest-api">https://pypi.org/project/csle-rest-api</a>
- <a href="https://pypi.org/project/csle-agents">https://pypi.org/project/csle-agents</a>
- <a href="https://pypi.org/project/csle-system-identification">https://pypi.org/project/csle-system-identification</a>
- <a href="https://pypi.org/project/csle-cli">https://pypi.org/project/csle-cli</a>
- <a href="https://pypi.org/project/csle-cluster">https://pypi.org/project/csle-cluster</a>
- <a href="https://pypi.org/project/gym-csle-intrusion-response-game">https://pypi.org/project/gym-csle-intrusion-response-game</a>
- <a href="https://pypi.org/project/csle-tolerance">https://pypi.org/project/csle-tolerance</a>
- <a href="https://pypi.org/project/csle-attack-profiler">https://pypi.org/project/csle-attack-profiler</a>


#### Lines of code

CSLE consists of around 275,000 lines of Python, 
40,000 lines of JavaScript, 
3000 lines of Dockerfiles, 
5400 lines of Makefile, 
14000 lines of Bash, 
and 7600 lines of YAML.
The lines of code can be counted by executing the following commands from the project root:
```bash
find . -name '*.py' | xargs wc -l
cd management-system/src; find . -name '*.js' | xargs wc -l
find . -name 'Dockerfile' | xargs wc -l
find . -name 'Makefile' | xargs wc -l
find . -name '*.sh' | xargs wc -l
find . -name '*.yml' | xargs wc -l
```
<p class="captionFig">
Listing 1: Commands for counting the lines of code in CSLE.
</p>

### Publications

Scientific publications related to CSLE are listed <a href="publications">here</a>.