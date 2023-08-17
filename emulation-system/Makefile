all: build

# Target for building all of the base images
base_images:
	cd base_images/ && $(MAKE) build

# Target for building all of the derived images
derived_images:
	cd derived_images/ && $(MAKE) build

# Target for installing all emulations
emulations:
	cd envs/ && $(MAKE) install

# Target for removing all of the derived images
rm_derived_images:
	cd derived_images/ && $(MAKE) rm_image

# Target for removing all of the base images (remove derived images first)
rm_base_images: rm_derived_images
	cd base_images/ && $(MAKE) rm_image

# Target for uninstalling all emulations
rm_emulations:
	cd envs/ && $(MAKE) uninstall

# Target for pushing all derived images to DockerHub
push_derived_images:
	cd derived_images/ && $(MAKE) push

# Target for pushing all base images to DockerHub
push_base_images:
	cd base_images/ && $(MAKE) push

# Target for pulling all derived images from DockerHub
pull_derived_images:
	cd derived_images/ && $(MAKE) pull

# Target for pulling all base images from DockerHub
pull_base_images:
	cd base_images/ && $(MAKE) pull

# Build emulation system
build: base_images derived_images emulations

install: pull_base_images pull_derived_images emulations

# Remove emulation system
rm: rm_emulations rm_derived_images rm_base_images

# Push all images to DockerHub
push: push_base_images push_derived_images

# Pull all images from DockerHub
pull: pull_base_images pull_derived_images

