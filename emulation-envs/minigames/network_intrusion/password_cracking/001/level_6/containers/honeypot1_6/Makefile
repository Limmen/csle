PROJECT=pycr
NETWORK=pycr_net_6
MINIGAME=pwcrack
CONTAINER=honeypot1
VERSION=0.0.1
LEVEL=6
IP=172.18.6.9
SUFFIX=_6
DIR=$(CURDIR)/../../
CFG=$(CURDIR)/../../containers.json
FLAGSCFG=$(CURDIR)/../../flags.json
TOPOLOGYCFG=$(CURDIR)/../../topology.json
USERSCFG=$(CURDIR)/../../users.json
VULNERABILITIESCFG=$(CURDIR)/../../vulnerabilities.json

all: run

run:
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER)$(SUFFIX)-level$(LEVEL) --net $(NETWORK) --ip $(IP) --label dir=$(DIR) --label containers_cfg=$(CFG) --label flags_cfg=$(FLAGSCFG) --label topology_cfg=$(TOPOLOGYCFG) --label users_cfg=$(USERSCFG) --label vulnerabilities_cfg=$(VULNERABILITIESCFG) --privileged -v /lib/modules:/lib/modules --cap-add NET_ADMIN --publish-all=true $(PROJECT)/$(CONTAINER):$(VERSION)

shell:
	docker exec -it $(PROJECT)-$(MINIGAME)-$(CONTAINER)$(SUFFIX)-level$(LEVEL) /bin/bash

start:
	docker container start $(PROJECT)-$(MINIGAME)-$(CONTAINER)$(SUFFIX)-level$(LEVEL)

# Stop running containers
stop:
	-docker stop $(PROJECT)-$(MINIGAME)-$(CONTAINER)$(SUFFIX)-level$(LEVEL)

# Stop and remove running containers
clean: stop
	-docker rm $(PROJECT)-$(MINIGAME)-$(CONTAINER)$(SUFFIX)-level$(LEVEL)
