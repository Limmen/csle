PROJECT=csle
CONTAINER=cve_2010_0426_base
VERSION=0.0.1

all: rm-image build

build: ./docker/Dockerfile
	docker build . -f ./docker/Dockerfile -t $(PROJECT)/$(CONTAINER):$(VERSION); cd ..

rm-image:
	-docker rmi $(PROJECT)/$(CONTAINER):$(VERSION)
