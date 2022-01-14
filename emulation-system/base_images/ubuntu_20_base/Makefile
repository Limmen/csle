PROJECT=csle
CONTAINER=ubuntu_20_base
VERSION=0.0.1
ROOT_USERS_FILE=root_users.txt
ROOT_USER_1=csle_admin
ROOT_PW_1=csle@admin-pw_191

all: rm-image build

# Creates the root admin user for configuring the container
users:
	echo "${ROOT_USER_1}:${ROOT_PW_1}" > ./docker/${ROOT_USERS_FILE}

# Build the docker container image. docker build <PATH to files to send to docker daemon> -f specifies the Dockerfile
# to use a recipe for the build. Use --no-cache to avoid build failures due to cached apt-get updates.
build: ./docker/Dockerfile users
	docker build . --no-cache -f ./docker/Dockerfile -t $(PROJECT)/$(CONTAINER):$(VERSION); cd ..

# Expunge old container image
rm-image:
	-docker rmi $(PROJECT)/$(CONTAINER):$(VERSION)