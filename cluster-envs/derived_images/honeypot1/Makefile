PROJECT=pycr
CONTAINER=honeypot1
VERSION=0.0.1

all: rm-image build net

build: ./docker/Dockerfile
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(CONTAINER):$(VERSION); cd ..

rm-image:
	-docker rmi $(PROJECT)/$(CONTAINER):$(VERSION)
