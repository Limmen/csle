all: build

kali_base:
	cd kali_base/ && $(MAKE) build

ubuntu_20_base:
	cd ubuntu_20_base/ && $(MAKE) build

ubuntu_14_base:
	cd ubuntu_14_base/ && $(MAKE) build

ssh_base:
	cd ssh_base/ && $(MAKE) build

build:
	cd kali_base/ && $(MAKE) build
	cd ubuntu_20_base/ && $(MAKE) build
	cd ubuntu_14_base/ && $(MAKE) build
	cd ssh_base/ && $(MAKE) build

rm-image:
	cd kali_base/ && $(MAKE) rm-image
	cd ubuntu_20_base/ && $(MAKE) rm-image
	cd ubuntu_14_base/ && $(MAKE) rm-image
	cd ssh_base/ && $(MAKE) rm-image