PROJECT=pycr
NETWORK=pycr_net_9
MINIGAME=ctf
CONTAINER=ssh1
VERSION=0.0.1
LEVEL=9
IP=172.18.9.2
DIR=$(CURDIR)/../../
CFG=$(CURDIR)/../../containers.json
FLAGSCFG=$(CURDIR)/../../flags.json
TOPOLOGYCFG=$(CURDIR)/../../topology.json
USERSCFG=$(CURDIR)/../../users.json
VULNERABILITIESCFG=$(CURDIR)/../../vulnerabilities.json
TRAFFICCFG=$(CURDIR)/../../traffic.json

all: run

run:
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) --hostname=$(CONTAINER) --net $(NETWORK) --ip $(IP) --label dir=$(DIR) --label containers_cfg=$(CFG) --label flags_cfg=$(FLAGSCFG) --label topology_cfg=$(TOPOLOGYCFG) --label users_cfg=$(USERSCFG) --label vulnerabilities_cfg=$(VULNERABILITIESCFG) --label traffic_cfg=$(TRAFFICCFG) --publish-all=true --cap-add NET_ADMIN $(PROJECT)/$(CONTAINER):$(VERSION)

shell:
	docker exec -it $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) /bin/bash

start:
	docker container start $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL)

# Stop running containers
stop:
	-docker stop $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL)

# Stop and remove running containers
clean: stop
	-docker rm $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL)
