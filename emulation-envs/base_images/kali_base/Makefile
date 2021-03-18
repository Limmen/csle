PROJECT=pycr
MINIGAME=pwcrack
CONTAINER=kali_base
VERSION=0.0.1
ROOT_USERS_FILE=root_users.txt
ROOT_USER_1=agent
ROOT_PW_1=agent
ROOT_USER_2=pycr_admin
ROOT_PW_2=pycr@admin-pw_191

all: rm-image build

users:
	echo "${ROOT_USER_1}:${ROOT_PW_1} ${ROOT_USER_2}:${ROOT_PW_2}" > ./docker/${ROOT_USERS_FILE}

build: ./docker/Dockerfile users
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(CONTAINER):$(VERSION); cd ..

# Expunge old container image
rm-image:
	-docker rmi $(PROJECT)/$(CONTAINER):$(VERSION)