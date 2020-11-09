PROJECT=pycr
CONTAINER=ubuntu_14_base
VERSION=0.0.1

all: rm-image rm-network build net

build: ./docker/Dockerfile
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(CONTAINER):$(VERSION); cd ..

# Expunge old container image
rm-image:
	-docker rmi $(PROJECT)/$(CONTAINER):$(VERSION)