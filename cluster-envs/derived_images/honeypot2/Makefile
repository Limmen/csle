PROJECT=pycr
CONTAINER=honeypot2
VERSION=0.0.1

all: rm-image build net

build: ./docker/Dockerfile
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(CONTAINER):$(VERSION); cd ..

rm-image:
	-docker rmi $(PROJECT)/$(MINIGAME)-$(CONTAINER)-level$(LEVEL):$(VERSION)
