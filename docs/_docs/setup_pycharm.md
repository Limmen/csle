---
title: Setup PyCharm
permalink: /docs/setup-pycharm/
---

## Setup PyCharm for Remote Development

The best way to debug and implement new features to the emulation system involves three steps: 
(1) deploy the latest version of the emulation system on your target cluster; 
(2) clone the latest source code both on the server and on your local machine (e.g. your laptop); 
(3) connect your Integrated Development Environment (IDE) to the cluster so that you can edit code directly on the cluster. 
This appendix walks through the steps of setting up the PyCharm IDE for remote development.

#### Step 1: Deploy CSLE on the servers.

Follow the instructions in the <a href="./../installing">here</a>.

#### Step 2: Clone the source code.

Run the following command on your local machine and on one of the servers where CSLE is installed:

```bash
git clone https://github.com/Limmen/csle
```
<p class="captionFig">
Listing 183: Command for cloning the source code of CSLE.
</p>

#### Step 3: Setup PyCharm for remote development.

Start PyCharm on your local machine and open the CSLE project. Next, go to "Preferences" in PyCharm (see Fig. 32).

<p align="center">
<img src="./../../img/pycharm_1.png" width="45%">
<p class="captionFig">
Figure 32: The preferences tab in PyCharm.
</p>
</p>

Then configure an SSH interpreter for the project by selecting the Python interpreter of the server where 
CSLE is installed (see Figs. 33-36).

<p align="center">
<img src="./../../img/pycharm_2.png" width="45%">
<p class="captionFig">
Figure 33: Configuration of a remote SSH Python interpreter in PyCharm (1/4).
</p>
</p>

<p align="center">
<img src="./../../img/pycharm_3.png" width="45%">
<p class="captionFig">
Figure 34: Configuration of a remote SSH Python interpreter in PyCharm (2/4).
</p>
</p>

<p align="center">
<img src="./../../img/pycharm_4.png" width="45%">
<p class="captionFig">
Figure 35: Configuration of a remote SSH Python interpreter in PyCharm (3/4).
</p>
</p>

<p align="center">
<img src="./../../img/pycharm_5.png" width="45%">
<p class="captionFig">
Figure 36: Configuration of a remote SSH Python interpreter in PyCharm (4/4).
</p>
</p>

To test that the remote SSH interpreter is working correctly and that the files are synchronized between the 
remote server and your local machine you can try to add a line of code in the IDE and verify that it also shows up 
on the server. You can also test the setup by running an example script in the `examples` folder.