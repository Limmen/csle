PROJECT=pycr
CONTAINER=samba_base
VERSION=0.0.1

all: rm-image build

pull:
	docker pull vulnerables/cve-2017-7494

build: ./docker/Dockerfile
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(CONTAINER):$(VERSION); cd ..

rm-image:
	-docker rmi $(PROJECT)/$(CONTAINER):$(VERSION)
