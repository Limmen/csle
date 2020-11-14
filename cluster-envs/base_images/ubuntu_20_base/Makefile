PROJECT=pycr
CONTAINER=ubuntu_20_base
VERSION=0.0.1
ROOT_USERS_FILE=root_users.txt
ROOT_USER_1=pycr_admin
ROOT_PW_1=pycr@admin-pw_191

all: rm-image rm-network build net

users:
	echo "${ROOT_USER_1}:${ROOT_PW_1}" > ./docker/${ROOT_USERS_FILE}

build: ./docker/Dockerfile users
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(CONTAINER):$(VERSION); cd ..

# Expunge old container image
rm-image:
	-docker rmi $(PROJECT)/$(CONTAINER):$(VERSION)