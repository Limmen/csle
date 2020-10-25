PROJECT=pycr
NETWORK=pycr_pwcrack_001_level_2_net
MINIGAME=pwcrack
CONTAINER=hacker-kali
VERSION=0.0.1
LEVEL=2
SUBNET=172.18.2.0
SUBNET_MASK_1=172.18.2.0/24
SUBNET_MASK_2=255.255.255.0
IP=172.18.2.191
ROOT_USERS_FILE=root_users.txt
ROOT_USER_1=agent
ROOT_PW_1=agent
ROUTER_IP=172.18.2.10
SETUP_FIREWALL_SCRIPT=setup_firewall.sh

all: rm-image rm-network build net

users:
	echo "${ROOT_USER_1}:${ROOT_PW_1}" > ./docker/${ROOT_USERS_FILE}

firewall:
	echo "#!/bin/bash\nroute add -net ${SUBNET} netmask ${SUBNET_MASK_2} gw ${ROUTER_IP}" > ./docker/${SETUP_FIREWALL_SCRIPT}

build: ./docker/Dockerfile users
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(MINIGAME)-$(CONTAINER)-level$(LEVEL):$(VERSION); cd ..

net:
	docker network create --subnet=$(SUBNET_MASK_1) $(NETWORK) || echo "network already created"

# --publish-all exposes all ports of the container
# -dt means detached and allocate tty
run: build net firewall
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) --net $(NETWORK) --ip $(IP) --cap-add NET_ADMIN --publish-all=true --privileged=true $(PROJECT)/$(MINIGAME)-$(CONTAINER)-level$(LEVEL):$(VERSION)

shell:
	docker exec -it $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) /bin/bash

# Start stopped containers
start:
	docker container start $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL)

# Stop running containers
stop:
	-docker stop $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL)

# Stop and remove running containers
clean: stop
	-docker rm $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL)

# Expunge old container image
rm-image:
	-docker rmi $(PROJECT)/$(MINIGAME)-$(CONTAINER)-level$(LEVEL):$(VERSION)

# remove network
rm-net:
	-docker network rm $(NETWORK)
