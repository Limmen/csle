all: build

kali_base:
	cd kali_base/ && $(MAKE) build

ubuntu_20_base:
	cd ubuntu_20_base/ && $(MAKE) build

ubuntu_14_base:
	cd ubuntu_14_base/ && $(MAKE) build

ssh_base:
	cd ssh_base/ && $(MAKE) build

samba_base:
	cd samba_base/ && $(MAKE) build

shellshock_base:
	cd shellshock_base/ && $(MAKE) build

sql_injection_base:
	cd sql_injection_base/ && $(MAKE) build

debian_jessie_base:
	cd debian_jessie_base/ && $(MAKE) build

cve_2015_3306_base:
	cd cve_2015_3306_base/ && $(MAKE) build

cve_2015_1427_base:
	cd cve_2015_1427_base/ && $(MAKE) build

cve_2016_10033_base:
	cd cve_2016_10033_base/ && $(MAKE) build

build:
	cd kali_base/ && $(MAKE) build
	cd ubuntu_20_base/ && $(MAKE) build
	cd ubuntu_14_base/ && $(MAKE) build
	cd ssh_base/ && $(MAKE) build
	cd samba_base/ && $(MAKE) build
	cd shellshock_base/ && $(MAKE) build
	cd sql_injection_base/ && $(MAKE) build
	cd debian_jessie_base/ && $(MAKE) build
	cd cve_2015_3306_base/ && $(MAKE) build
	cd cve_2015_1427_base/ && $(MAKE) build
	cd cve_2016_10033_base/ && $(MAKE) build

rm-image:
	cd kali_base/ && $(MAKE) rm-image
	cd ubuntu_20_base/ && $(MAKE) rm-image
	cd ubuntu_14_base/ && $(MAKE) rm-image
	cd ssh_base/ && $(MAKE) rm-image
	cd samba_base/ && $(MAKE) rm-image
	cd shellshock_base/ && $(MAKE) rm-image
	cd sql_injection_base/ && $(MAKE) rm-image
	cd debian_jessie_base/ && $(MAKE) rm-image
	cd cve_2015_3306_base/ && $(MAKE) rm-image
	cd cve_2015_1427_base/ && $(MAKE) rm-image
	cd cve_2016_10033_base/ && $(MAKE) rm-image