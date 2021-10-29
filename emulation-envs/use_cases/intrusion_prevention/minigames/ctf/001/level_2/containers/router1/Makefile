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

all: run

run:
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) --hostname=$(CONTAINER) --net $(NETWORK) --ip $(IP) --label dir=$(DIR) --label containers_cfg=$(CFG) --label flags_cfg=$(FLAGSCFG) --label topology_cfg=$(TOPOLOGYCFG) --label users_cfg=$(USERSCFG) --label vulnerabilities_cfg=$(VULNERABILITIESCFG) --label traffic_cfg=$(TRAFFICCFG) --publish-all=true --privileged -v /lib/modules:/lib/modules --cap-add NET_ADMIN $(PROJECT)/$(CONTAINER):$(VERSION)

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
