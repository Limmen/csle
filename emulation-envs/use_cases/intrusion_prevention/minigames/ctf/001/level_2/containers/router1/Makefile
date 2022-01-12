PROJECT=pycr
NETWORK=pycr_net_2
MINIGAME=ctf
CONTAINER=router1
VERSION=0.0.1
IP=172.18.2.10
LEVEL=2
DIR=../../
CFG=../../containers.json
FLAGSCFG=../../flags.json
TOPOLOGYCFG=../../topology.json
USERSCFG=../../users.json
VULNERABILITIESCFG=../../vulnerabilities.json
TRAFFICCFG=$(CURDIR)/../../traffic.json
RESTART_POLICY="on-failure:3"
NUM_CPUS=1
MEMORY='4G'

all: run

# Create and start the container
run:
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) --hostname=$(CONTAINER) \
	--net $(NETWORK) --ip $(IP) --label dir=$(DIR) --label containers_cfg=$(CFG) \
	--label flags_cfg=$(FLAGSCFG) --label topology_cfg=$(TOPOLOGYCFG) --label users_cfg=$(USERSCFG) \
	--label vulnerabilities_cfg=$(VULNERABILITIESCFG) --label traffic_cfg=$(TRAFFICCFG) \
	--publish-all=true --privileged -v /lib/modules:/lib/modules \
	--memory=$(MEMORY) --cpus=$(NUM_CPUS) --restart=$(RESTART_POLICY) \
	--cap-add NET_ADMIN $(PROJECT)/$(CONTAINER):$(VERSION)

# Start a bash session inside the container (assumes that the container is already started)
shell:
	docker exec -it $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) /bin/bash

# Starts the container (assumes that it has previously been created and stopped)
start:
	docker container start $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL)

# Stop the container
stop:
	-docker stop $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL)

# Stop and remove the container
clean: stop
	-docker rm $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL)
