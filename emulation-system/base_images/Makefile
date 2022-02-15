PROJECT=csle
VERSION=0.0.1

.PHONY: all build rm_image kali_base ubuntu_20_base ubuntu_14_base ssh_base samba_base \
	shellshock_base sql_injection_base \
	debian_jessie_base cve_2015_3306_base cve_2015_1427_base cve_2016_10033_base cve_2010_0426_base cve_2015_5602_base \
	blank_ubuntu_20 pengine_exploit_base rm_kali_base rm_ubuntu_20_base rm_ubuntu_14_base rm_ssh_base rm_samba_base \
	rm_shellshock_base rm_sql_injection_base rm_debian_jessie_base rm_cve_2015_3306_base rm_cve_2015_1427_base \
	rm_cve_2016_10033_base rm_cve_2010_0426_base rm_cve_2015_5602_base \
	rm_blank_ubuntu_20 rm_pengine_exploit_base cve_2014_0160_base rm_cve_2014_0160_base

all: build

# Targets for building all of the base images
kali_base:
	docker build . --no-cache -f ./docker_files/kali_base/docker/Dockerfile -t $(PROJECT)/kali_base:$(VERSION)

ubuntu_20_base:
	docker build . --no-cache -f ./docker_files/ubuntu_20_base/docker/Dockerfile -t $(PROJECT)/ubuntu_20_base:$(VERSION)

ubuntu_14_base:
	docker build . --no-cache -f ./docker_files/ubuntu_14_base/docker/Dockerfile -t $(PROJECT)/ubuntu_14_base:$(VERSION)

ssh_base:
	docker build . --no-cache -f ./docker_files/ssh_base/docker/Dockerfile -t $(PROJECT)/ssh_base:$(VERSION)

samba_base:
	docker build . --no-cache -f ./docker_files/samba_base/docker/Dockerfile -t $(PROJECT)/samba_base:$(VERSION)

shellshock_base:
	docker build . --no-cache -f ./docker_files/shellshock_base/docker/Dockerfile -t $(PROJECT)/shellshock_base:$(VERSION)

sql_injection_base:
	docker build . --no-cache -f ./docker_files/sql_injection_base/docker/Dockerfile -t $(PROJECT)/sql_injection_base:$(VERSION)

debian_jessie_base:
	docker build . --no-cache -f ./docker_files/debian_jessie_base/docker/Dockerfile -t $(PROJECT)/debian_jessie_base:$(VERSION)

cve_2015_3306_base:
	docker build . --no-cache -f ./docker_files/cve_2015_3306_base/docker/Dockerfile -t $(PROJECT)/cve_2015_3306_base:$(VERSION)

cve_2015_1427_base:
	docker build . --no-cache -f ./docker_files/cve_2015_1427_base/docker/Dockerfile -t $(PROJECT)/cve_2015_1427_base:$(VERSION)

cve_2016_10033_base:
	docker build . --no-cache -f ./docker_files/cve_2016_10033_base/docker/Dockerfile -t $(PROJECT)/cve_2016_10033_base:$(VERSION)

cve_2010_0426_base:
	docker build . --no-cache -f ./docker_files/cve_2010_0426_base/docker/Dockerfile -t $(PROJECT)/cve_2010_0426_base:$(VERSION)

cve_2015_5602_base:
	docker build . --no-cache -f ./docker_files/cve_2015_5602_base/docker/Dockerfile -t $(PROJECT)/cve_2015_5602_base:$(VERSION)

blank_ubuntu_20:
	docker build . --no-cache -f ./docker_files/blank_ubuntu_20/docker/Dockerfile -t $(PROJECT)/blank_ubuntu_20:$(VERSION)

pengine_exploit_base:
	docker build . --no-cache -f ./docker_files/pengine_exploit_base/docker/Dockerfile -t $(PROJECT)/pengine_exploit_base:$(VERSION)

cve_2014_0160_base:
	docker build . --no-cache -f ./docker_files/cve_2014_0160_base/docker/Dockerfile -t $(PROJECT)/cve_2014_0160_base:$(VERSION)

# Targets for removing all of the base images
rm_kali_base:
	-docker rmi $(PROJECT)/kali_base:$(VERSION)

rm_ubuntu_20_base:
	-docker rmi $(PROJECT)/ubuntu_20_base:$(VERSION)

rm_ubuntu_14_base:
	-docker rmi $(PROJECT)/ubuntu_14_base:$(VERSION)

rm_ssh_base:
	-docker rmi $(PROJECT)/ssh_base:$(VERSION)

rm_samba_base:
	-docker rmi $(PROJECT)/samba_base:$(VERSION)

rm_shellshock_base:
	-docker rmi $(PROJECT)/shellshock_base:$(VERSION)

rm_sql_injection_base:
	-docker rmi $(PROJECT)/sql_injection_base:$(VERSION)

rm_debian_jessie_base:
	-docker rmi $(PROJECT)/debian_jessie_base:$(VERSION)

rm_cve_2015_3306_base:
	-docker rmi $(PROJECT)/cve_2015_3306_base:$(VERSION)

rm_cve_2015_1427_base:
	-docker rmi $(PROJECT)/cve_2015_1427_base:$(VERSION)

rm_cve_2016_10033_base:
	-docker rmi $(PROJECT)/cve_2016_10033_base:$(VERSION)

rm_cve_2010_0426_base:
	-docker rmi $(PROJECT)/cve_2010_0426_base:$(VERSION)

rm_cve_2015_5602_base:
	-docker rmi $(PROJECT)/cve_2015_5602_base:$(VERSION)

rm_blank_ubuntu_20:
	-docker rmi $(PROJECT)/blank_ubuntu_20:$(VERSION)

rm_pengine_exploit_base:
	-docker rmi $(PROJECT)/pengine_exploit_base:$(VERSION)

rm_cve_2014_0160_base:
	-docker rmi $(PROJECT)/cve_2014_0160_base:$(VERSION)

# Build all of the base images sequentially
build:
	docker build . --no-cache -f ./docker_files/kali_base/docker/Dockerfile -t $(PROJECT)/kali_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/ubuntu_20_base/docker/Dockerfile -t $(PROJECT)/ubuntu_20_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/ubuntu_14_base/docker/Dockerfile -t $(PROJECT)/ubuntu_14_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/ssh_base/docker/Dockerfile -t $(PROJECT)/ssh_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/samba_base/docker/Dockerfile -t $(PROJECT)/samba_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/shellshock_base/docker/Dockerfile -t $(PROJECT)/shellshock_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/sql_injection_base/docker/Dockerfile -t $(PROJECT)/sql_injection_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/debian_jessie_base/docker/Dockerfile -t $(PROJECT)/debian_jessie_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/cve_2015_3306_base/docker/Dockerfile -t $(PROJECT)/cve_2015_3306_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/cve_2015_1427_base/docker/Dockerfile -t $(PROJECT)/cve_2015_1427_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/cve_2016_10033_base/docker/Dockerfile -t $(PROJECT)/cve_2016_10033_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/cve_2010_0426_base/docker/Dockerfile -t $(PROJECT)/cve_2010_0426_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/cve_2015_5602_base/docker/Dockerfile -t $(PROJECT)/cve_2015_5602_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/blank_ubuntu_20/docker/Dockerfile -t $(PROJECT)/blank_ubuntu_20:$(VERSION)
	docker build . --no-cache -f ./docker_files/pengine_exploit_base/docker/Dockerfile -t $(PROJECT)/pengine_exploit_base:$(VERSION)

# Remove all base images
rm_image:
	-docker rmi $(PROJECT)/kali_base:$(VERSION)
	-docker rmi $(PROJECT)/ubuntu_20_base:$(VERSION)
	-docker rmi $(PROJECT)/ubuntu_14_base:$(VERSION)
	-docker rmi $(PROJECT)/ssh_base:$(VERSION)
	-docker rmi $(PROJECT)/samba_base:$(VERSION)
	-docker rmi $(PROJECT)/shellshock_base:$(VERSION)
	-docker rmi $(PROJECT)/sql_injection_base:$(VERSION)
	-docker rmi $(PROJECT)/debian_jessie_base:$(VERSION)
	-docker rmi $(PROJECT)/cve_2015_3306_base:$(VERSION)
	-docker rmi $(PROJECT)/cve_2015_1427_base:$(VERSION)
	-docker rmi $(PROJECT)/cve_2016_10033_base:$(VERSION)
	-docker rmi $(PROJECT)/cve_2010_0426_base:$(VERSION)
	-docker rmi $(PROJECT)/cve_2015_5602_base:$(VERSION)
	-docker rmi $(PROJECT)/blank_ubuntu_20:$(VERSION)
	-docker rmi $(PROJECT)/pengine_exploit_base:$(VERSION)
	-docker rmi $(PROJECT)/cve_2014_0160_base:$(VERSION)
