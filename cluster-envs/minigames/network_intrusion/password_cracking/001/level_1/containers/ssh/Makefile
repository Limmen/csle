PROJECT=pycr
NETWORK=pycr_pwcrack_001_level_1_net
MINIGAME=pwcrack
CONTAINER=ssh
VERSION=0.0.1
LEVEL=1
SUBNET=172.18.1.0
SUBNET_MASK_1=172.18.1.0/24
SUBNET_MASK_2=255.255.255.0
IP=172.18.1.2
ROOT_USERS_FILE=root_users.txt
NON_ROOT_USERS_FILE=non_root_users.txt
ROOT_USER_1=admin
ROOT_PW_1=test32121
ROOT_USER_2=user1
ROOT_PW_2=123123
NON_ROOT_USER_1=puppet
NON_ROOT_PW_1=puppet
FLAG_INFO_FILE=fl_info.txt
FLAG_PATH_1=/tmp
FLAG_NAME_1=flag2

all: rm-image rm-network build net

users:
	echo "${ROOT_USER_1}:${ROOT_PW_1} ${ROOT_USER_2}:${ROOT_PW_2}" > ./docker/${ROOT_USERS_FILE}
	echo "${NON_ROOT_USER_1}:${NON_ROOT_PW_1}" > ./docker/${NON_ROOT_USERS_FILE}

flags:
	echo "${FLAG_PATH_1}:${FLAG_NAME_1}" > ./docker/${FLAG_INFO_FILE}

build: ./docker/Dockerfile users flags
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(MINIGAME)-$(CONTAINER)-level$(LEVEL):$(VERSION); cd ..

net:
	docker network create --subnet=$(SUBNET_MASK_1) $(NETWORK) || echo "network already created"

# --publish-all exposes all ports of the container
run: build net
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) --net $(NETWORK) --ip $(IP) --publish-all=true $(PROJECT)/$(MINIGAME)-$(CONTAINER)-level$(LEVEL):$(VERSION)

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
