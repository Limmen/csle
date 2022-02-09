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

# Build all images
build: base_images derived_images

# Remove all base images
rm: rm_emulations rm_base_images

