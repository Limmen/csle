PROJECT=pycr
NETWORK=pycr_pwcrack_001_level_2_net
MINIGAME=pwcrack
CONTAINER=router
VERSION=0.0.1
SUBNET=172.18.2.0
SUBNET_MASK_1=172.18.2.0/24
SUBNET_MASK_2=255.255.255.0
IP=172.18.2.10
LEVEL=2
ROOT_USERS_FILE=root_users.txt
NON_ROOT_USERS_FILE=non_root_users.txt
ROOT_USER_1=admin
ROOT_PW_1=admin
NON_ROOT_USER_1=jessica
NON_ROOT_PW_1=water
FLAG_INFO_FILE=fl_info.txt
FLAG_PATH_1=/home/admin
FLAG_NAME_1=flag0

all: clean rm-image rm-net build net run

users:
	echo "${ROOT_USER_1}:${ROOT_PW_1}" > ./docker/${ROOT_USERS_FILE}
	echo "${NON_ROOT_USER_1}:${NON_ROOT_PW_1}" > ./docker/${NON_ROOT_USERS_FILE}

flags:
	echo "${FLAG_PATH_1}:${FLAG_NAME_1}" > ./docker/${FLAG_INFO_FILE}

build: ./docker/Dockerfile users flags
	docker build . --no-cache -f ./docker/Dockerfile -t $(PROJECT)/$(MINIGAME)-$(CONTAINER)-level$(LEVEL):$(VERSION); cd ..


net:
	docker network create --subnet=$(SUBNET_MASK_1) $(NETWORK) || echo "network already created"

# --publish-all exposes all ports of the container
# route -n to list routes
run: build net
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER)-level$(LEVEL) --net $(NETWORK) --ip $(IP) --publish-all=true $(PROJECT)/$(MINIGAME)-$(CONTAINER)-level$(LEVEL):$(VERSION)
#	./setup_firewall.sh $(SUBNET) $(SUBNET_MASK_2) $(IP)

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
