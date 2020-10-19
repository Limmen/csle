PROJECT=pycr
NETWORK=pycr_net
MINIGAME=pwcrack
CONTAINER=ftp
VERSION=0.0.1
SUBNET=172.18.1.0
SUBNET_MASK_1=172.18.1.0/24
SUBNET_MASK_2=255.255.255.0
IP=172.18.1.79
ROOT_USERS_FILE=root_users.txt
NON_ROOT_USERS_FILE=non_root_users.txt
ROOT_USER_1=l_hopital
ROOT_PW_1=l_hopital
ROOT_USER_2=pi
ROOT_PW_2=pi
NON_ROOT_USER_1=euler
NON_ROOT_PW_1=euler
FLAG_INFO_FILE=fl_info.txt
FLAG_PATH_1=/tmp
FLAG_NAME_1=flag3
#FLAG_PATH_2=/root
#FLAG_NAME2=flag4

all: rm-image rm-network build net

users:
	echo "${ROOT_USER_1}:${ROOT_PW_1} ${ROOT_USER_2}:${ROOT_PW_2}" > ./docker/${ROOT_USERS_FILE}
	echo "${NON_ROOT_USER_1}:${NON_ROOT_PW_1}" > ./docker/${NON_ROOT_USERS_FILE}

flags:
	echo "${FLAG_PATH_1}:${FLAG_NAME_1}" > ./docker/${FLAG_INFO_FILE}

build: ./docker/Dockerfile users flags
	docker build . --no-cache -f ./docker/Dockerfile -t $(PROJECT)/$(MINIGAME)-$(CONTAINER):$(VERSION); cd ..

net:
	docker network create --subnet=$(SUBNET_MASK_1) $(NETWORK) || echo "network already created"

# --publish-all exposes all ports of the container
run: build net
	docker container run -dt --name $(PROJECT)-$(MINIGAME)-$(CONTAINER) --net $(NETWORK) --ip $(IP) --publish-all=true $(PROJECT)/$(MINIGAME)-$(CONTAINER):$(VERSION)

shell:
	docker exec -it $(PROJECT)-$(MINIGAME)-$(CONTAINER) /bin/bash

# Stop running containers
stop:
	-docker stop $(PROJECT)-$(MINIGAME)-$(CONTAINER)

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
