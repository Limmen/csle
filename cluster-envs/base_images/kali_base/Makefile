PROJECT=pycr
MINIGAME=pwcrack
CONTAINER=kali_base
VERSION=0.0.1
ROOT_USERS_FILE=root_users.txt
ROOT_USER_1=agent
ROOT_PW_1=agent

all: rm-image build

users:
	echo "${ROOT_USER_1}:${ROOT_PW_1}" > ./docker/${ROOT_USERS_FILE}

build: ./docker/Dockerfile users
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(CONTAINER):$(VERSION); cd ..

# Expunge old container image
rm-image:
	-docker rmi $(PROJECT)/$(CONTAINER):$(VERSION)