PROJECT=pycr
NETWORK=pycr_net
MINIGAME=pwcrack
CONTAINER=router
VERSION=0.0.1
SUBNET=172.18.1.0
SUBNET_MASK_1=172.18.1.0/24
SUBNET_MASK_2=255.255.255.0
IP=172.18.1.10
ROOT_USERS_FILE=root_users.txt
NON_ROOT_USERS_FILE=non_root_users.txt
ROOT_USER_1=admin
ROOT_PW_1=admin
NON_ROOT_USER_1=jessica
NON_ROOT_PW_1=water
FLAG_INFO_FILE=flag_info.txt
FLAG_PATH_1=/home/admin
FLAG_NAME_1=flag0

all: rm-image rm-network build net

users:
	echo "${ROOT_USER_1}:${ROOT_PW_1}" > ./docker/${ROOT_USERS_FILE}
	echo "${NON_ROOT_USER_1}:${NON_ROOT_PW_1}" > ./docker/${NON_ROOT_USERS_FILE}

flags:
	echo "${FLAG_PATH_1}:${FLAG_NAME_1}" > ./docker/${FLAG_INFO_FILE}

build: ./docker/Dockerfile users flags
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(MINIGAME)-$(CONTAINER):$(VERSION); cd ..


net:
	docker network create --subnet=$(SUBNET_MASK_1) $(NETWORK) || echo "network already created"

# --publish-all exposes all ports of the container
# route -n to list routes
run: build net
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER) --net $(NETWORK) --ip $(IP) --publish-all=true $(PROJECT)/$(MINIGAME)-$(CONTAINER):$(VERSION)
	./setup_firewall.sh

shell:
	docker exec -it $(PROJECT)-$(MINIGAME)-$(CONTAINER) /bin/bash

# Stop and remove running containers
clean:
	-docker stop $(PROJECT)-$(MINIGAME)-$(CONTAINER)
	-docker rm $(PROJECT)-$(MINIGAME)-$(CONTAINER)

# Expunge old container image
rm-image:
	-docker rmi $(PROJECT)/$(MINIGAME)-$(CONTAINER):$(VERSION)

# remove network
rm-net:
	-docker network rm $(NETWORK)
