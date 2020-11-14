PROJECT=pycr
NETWORK=pycr_pwcrack_001_level_1_net
MINIGAME=pwcrack
CONTAINER=honeypot
VERSION=0.0.1
LEVEL=1
SUBNET=172.18.1.0
SUBNET_MASK_1=172.18.1.0/24
SUBNET_MASK_2=255.255.255.0
IP=172.18.1.21
ROOT_USERS_FILE=root_users.txt
NON_ROOT_USERS_FILE=non_root_users.txt
ROOT_USER_1=admin
ROOT_PW_1=admin
ROOT_USER_2=test
ROOT_PW_2=qwerty
NON_ROOT_USER_1=oracle
NON_ROOT_PW_1=abc123

all: rm-image rm-network build net

users:
	echo "${ROOT_USER_1}:${ROOT_PW_1} ${ROOT_USER_2}:${ROOT_PW_2}" > ./docker/${ROOT_USERS_FILE}
	echo "${NON_ROOT_USER_1}:${NON_ROOT_PW_1}" > ./docker/${NON_ROOT_USERS_FILE}

build: ./docker/Dockerfile users
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(MINIGAME)-$(CONTAINER)-level$(LEVEL):$(VERSION); cd ..

net:
	docker network create --subnet=$(SUBNET_MASK_1) $(NETWORK) || echo "network already created"

# --publish-all exposes all ports of the container
run: build net
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) --net $(NETWORK) --ip $(IP) --publish-all=true --cap-add NET_ADMIN $(PROJECT)/$(MINIGAME)-$(CONTAINER)-level$(LEVEL):$(VERSION)

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

# Expunge old container image
rm-image:
	-docker rmi $(PROJECT)/$(MINIGAME)-$(CONTAINER)-level$(LEVEL):$(VERSION)

# remove network
rm-net:
	-docker network rm $(NETWORK)
