PROJECT=pycr
NETWORK=pycr_net_1
MINIGAME=ctf
CONTAINER=ftp1
VERSION=0.0.1
LEVEL=1
IP=172.18.1.79
DIR:=$(CURDIR)/../../
CFG:=$(CURDIR)/../../containers.json
FLAGSCFG:=$(CURDIR)/../../flags.json
TOPOLOGYCFG:=$(CURDIR)/../../topology.json
USERSCFG:=$(CURDIR)/../../users.json
VULNERABILITIESCFG:=$(CURDIR)/../../vulnerabilities.json
TRAFFICCFG:=$(CURDIR)/../../traffic.json
RESTART_POLICY="on-failure:3"
NUM_CPUS=1
MEMORY=4G

# NOTE! that bps refers to BYTES/S in this case! i.e to get 1 000 000 bit per second, use 1/8=0.125mbps
# LAN
LAN_RATE_LIMIT=1tbit
LAN_OUTGOING_PACKETS_TRANSMISSION_DELAY=100us
LAN_OUTGOING_PACKET_LOSS_PERCENTAGE=0.000001%
LAN_OUTGOING_PACKET_DUPLICATE_PERCENTAGE=0.000001%
LAN_OUTGOING_PACKET_CORRUPT_PERCENTAGE=0.000001%

# Internet
INTERNET_RATE_LIMIT=100mbit
INTERNET_OUTGOING_PACKETS_TRANSMISSION_DELAY=100us
INTERNET_OUTGOING_PACKET_LOSS_PERCENTAGE=0.03%
INTERNET_OUTGOING_PACKET_DUPLICATE_PERCENTAGE=0.001%
INTERNET_OUTGOING_PACKET_CORRUPT_PERCENTAGE=0.02%

all: run

# Create and start the container
run:
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) --hostname=$(CONTAINER) \
	--net $(NETWORK) --ip $(IP) --label dir=$(DIR) --label containers_cfg=$(CFG) --label flags_cfg=$(FLAGSCFG) \
	--label topology_cfg=$(TOPOLOGYCFG) --label users_cfg=$(USERSCFG) \
	--label vulnerabilities_cfg=$(VULNERABILITIESCFG) --label traffic_cfg=$(TRAFFICCFG) \
	--publish-all=true --privileged -v /lib/modules:/lib/modules \
	--memory=$(MEMORY) --cpus=$(NUM_CPUS) --restart=$(RESTART_POLICY) \
	--label com.docker-tc.enabled=1 \
	--label com.docker-tc.limit=$(LAN_RATE_LIMIT) \
	--label com.docker-tc.delay=$(LAN_OUTGOING_PACKETS_TRANSMISSION_DELAY) \
	--label com.docker-tc.loss=$(LAN_OUTGOING_PACKET_LOSS_PERCENTAGE) \
	--label com.docker-tc.duplicate=$(LAN_OUTGOING_PACKET_DUPLICATE_PERCENTAGE) \
	--label com.docker-tc.corrupt=$(LAN_OUTGOING_PACKET_CORRUPT_PERCENTAGE) \
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
clean:
	-docker stop $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL)
	-docker rm $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL)
