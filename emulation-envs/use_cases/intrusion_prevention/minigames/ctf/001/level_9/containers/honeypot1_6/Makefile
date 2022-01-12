PROJECT=pycr
NETWORK=pycr_net_9
MINIGAME=ctf
CONTAINER=honeypot1
VERSION=0.0.1
LEVEL=9
IP=172.18.9.9
SUFFIX=_6
DIR=$(CURDIR)/../../
CFG=$(CURDIR)/../../containers.json
FLAGSCFG=$(CURDIR)/../../flags.json
TOPOLOGYCFG=$(CURDIR)/../../topology.json
USERSCFG=$(CURDIR)/../../users.json
VULNERABILITIESCFG=$(CURDIR)/../../vulnerabilities.json
TRAFFICCFG=$(CURDIR)/../../traffic.json
RESTART_POLICY="on-failure:3"
NUM_CPUS=1
MEMORY='4G'

all: run

run:
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) --hostname=$(CONTAINER) \
	--net $(NETWORK) --ip $(IP) --label dir=$(DIR) --label containers_cfg=$(CFG) --label flags_cfg=$(FLAGSCFG) \
	--label topology_cfg=$(TOPOLOGYCFG) --label users_cfg=$(USERSCFG) \
	--label vulnerabilities_cfg=$(VULNERABILITIESCFG) \
	--label traffic_cfg=$(TRAFFICCFG) --publish-all=true \
	--memory=$(MEMORY) --cpus=$(NUM_CPUS) --restart=$(RESTART_POLICY) \
	--cap-add NET_ADMIN $(PROJECT)/$(CONTAINER):$(VERSION)

# Start a bash session inside the container (assumes that the container is already started)
shell:
	docker exec -it $(PROJECT)-$(MINIGAME)-$(CONTAINER)$(SUFFIX)-level$(LEVEL) /bin/bash

# Starts the container (assumes that it has previously been created and stopped)
start:
	docker container start $(PROJECT)-$(MINIGAME)-$(CONTAINER)$(SUFFIX)-level$(LEVEL)

# Stop running containers
stop:
	-docker stop $(PROJECT)-$(MINIGAME)-$(CONTAINER)$(SUFFIX)-level$(LEVEL)

# Stop and remove running containers
clean: stop
	-docker rm $(PROJECT)-$(MINIGAME)-$(CONTAINER)$(SUFFIX)-level$(LEVEL)
