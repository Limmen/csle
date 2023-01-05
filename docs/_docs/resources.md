---
title: Resources
permalink: /docs/resources/
---

## Resources

Resources for getting started with CSLE are described below.

### Documentation
Apart from the web documentation (i.e the documentation you are reading now), which is available at
<a href="https://limmen.dev/csle/">https://limmen.dev/csle/</a>, there are official release documents, 
which are available in PDF format for each release <a href="https://github.com/Limmen/csle/tree/master/releases">here</a>. 
A video demonstration of an earlier version of CSLE is available on 
<a href="https://www.youtube.com/watch?v=18P7MjPKNDg&t=1s">Youtube</a>.

### Source code, Binaries, and Docker Images

The source code of CSLE is available on GitHub:
<a href="https://github.com/Limmen/csle">https://github.com/Limmen/csle</a> and the Docker images are 
available on DockerHub:
<a href="https://hub.docker.com/u/kimham">https://hub.docker.com/u/kimham</a>. 
Further, binaries of the Python libraries in CSLE are available on PyPi:

- <a href="https://pypi.org/project/csle-collector">https://pypi.org/project/csle-collector</a>
- <a href="https://pypi.org/project/csle-common">https://pypi.org/project/csle-common</a>
- <a href="https://pypi.org/project/csle-attacker">https://pypi.org/project/csle-attacker</a>
- <a href="https://pypi.org/project/csle-defender">https://pypi.org/project/csle-defender</a>
- <a href="https://pypi.org/project/gym-csle-stopping-game">https://pypi.org/project/gym-csle-stopping-game</a>
- <a href="https://pypi.org/project/csle-ryu">https://pypi.org/project/csle-ryu</a>
- <a href="https://pypi.org/project/csle-rest-api">https://pypi.org/project/csle-rest-api</a>
- <a href="https://pypi.org/project/csle-agents">https://pypi.org/project/csle-agents</a>
- <a href="https://pypi.org/project/csle-system-identification">https://pypi.org/project/csle-system-identification</a>
- <a href="https://pypi.org/project/csle-cli">https://pypi.org/project/csle-cli</a>


#### Lines of code

CSLE consists of around 120,000 lines of Python \cite{van1995python}, 
30,000 lines of JavaScript, 
2,500 lines of Dockerfiles, 
1,400 lines of Makefile, 
and 1,600 lines of Bash. 
The lines of code can be counted by executing the following commands from the project root:
```bash
find . -name '*.py' | xargs wc -l
find . -name '*.js' | xargs wc -l
find . -name 'Dockerfile' | xargs wc -l
find . -name 'Makefile' | xargs wc -l
find . -name '*.sh' | xargs wc -l
```
<p class="captionFig">
Listing 1: Commands for counting the lines of code in CSLE.
</p>

### Publications

Scientific publications related to CSLE are listed <a href="publications">here</a>.