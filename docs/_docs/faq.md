---
title: Frequently Asked Questions
permalink: /docs/faq/
---

## Frequently Asked Questions

**Q: How to add a new management user?**

**A:** New management users can be added by administrators through the web interface.

**Q: Why does my machine crash when I try to run the emulation environment `csle-level9-010`?**

**A:** Most likely because the machine is running out of memory. The emulation environment `csle-level9-010` includes 34 containers, each of which requires at least 1GB of RAM, meaning that the machine needs at least 34GB of RAM to run this emulation environment.

**Q: Why does my reinforcement learning algorithm not converge?**

**A:** Why does my reinforcement learning algorithm not converge?There are many possible reasons for this; it could be a hyperparameter problem, a bug in your training environment, or simply slow convergence. These issues are not related to CSLE's implementation.

**Q: How can I use CSLE with my own custom code?**

**A:** You have two options. One option is to integrate your code with CSLE as a new simulation or emulation environment. Another option is that you write custom code to integrate CSLE with your existing code base. The latter option is not something that CSLE maintainers will provide support for.

**Q: How do I generate plots?**

**A:** CSLE does not have its own plotting library. Plots can be created through standard libraries, e.g., matplotlib.

**Q: How do I install CSLE?**

**A:** See the instructions <a href="../installing">here</a>

**Q: Can I install CSLE on Windows?**

**A:** No.

**Q: Can I install CSLE on Mac?** 

**A:** Yes, you should be able to take the installation instructions for Linux and adapt them to a Mac environment. Note that Mac is not a platform that is actively supported in CSLE. Hence, you can not expect help from maintainers if you run into Mac-specific issues.

**Q: How do I use the Docker images in CSLE without the rest of the framework?**

**A:** The CSLE Docker images can be pulled as standalone images from <a href="https://hub.docker.com/r/kimham/">DockerHub</a>.

**Q: How do I cite CSLE?**

**A:** A list of publications is available <a href="../../publications">here</a>

**Q: Can I use CSLE for commercial purposes?**

**A:** Yes if it is compatible with the license (Creative Commons Attribution-ShareAlike 4.0 International License).

**Q: Can I use CSLE for research purposes?**

**A:** Yes, CSLE was built for research purposes. If you use CSLE in your research please cite us.

**Q: Can I use CSLE in an air-gapped environment?**

**A:** An air-gapped installation is possible but is not something that is officially supported in CSLE.

**Q: Can I run CSLE in the cloud?**

**A:** Yes you can deploy CSLE on virtual machines provided by any cloud vendor.

**Q: Can I take the CSLE code as a base to develop a new framework?**

**A:** Yes as long as you respect the license (Creative Commons Attribution-ShareAlike 4.0 International License).

**Q: Can I deploy CSLE on a Kubernetes cluster?**

**A:** It is possible but it is not something that we have documentation for.

**Q: How can I contribute to CSLE?**

**A:** See the developer guide <a href="../development-conventions">here</a>.

**Q: How can I contact the maintainers of CSLE?**

**A:** Contact us via the <a href="https://github.com/Limmen/csle/issues">GitHub issues page</a>
