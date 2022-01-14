PROJECT=csle
CONTAINER=cve_2015_3306_base
VERSION=0.0.1

all: rm-image build

# Build the docker container image. docker build <PATH to files to send to docker daemon> -f specifies the Dockerfile
# to use a recipe for the build. Use --no-cache to avoid build failures due to cached apt-get updates.
build: ./docker/Dockerfile
	docker build . --no-cache -f ./docker/Dockerfile -t $(PROJECT)/$(CONTAINER):$(VERSION); cd ..

# Expunge old container image
rm-image:
	-docker rmi $(PROJECT)/$(CONTAINER):$(VERSION)
