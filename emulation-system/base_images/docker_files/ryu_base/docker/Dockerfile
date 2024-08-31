# OS
FROM kimham/csle_ubuntu_20_base:0.7.0
USER root

# RYU
SHELL ["conda", "run", "-n", "base", "/bin/bash", "-c"]
RUN pip install ryu eventlet==0.30.2 csle-ryu

# Controller start script
ADD docker_files/common/ryu_controller.py /ryu_controller.py
RUN chmod 777 /ryu_controller.py

# Topology GUI HTML files
ADD docker_files/ryu_base/html /root/miniconda3/lib/python3.9/site-packages/ryu/app/gui_topology/html