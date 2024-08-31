DOCKERHUB_USER=kimham
VERSION=0.7.0

.PHONY: all build rm_image kali_base ubuntu_20_base ubuntu_22_base ubuntu_14_base ssh_base samba_base \
	shellshock_base shellshock_debian_wheezy_base sql_injection_base \
	debian_10_base cve_2015_3306_base cve_2015_1427_base cve_2016_10033_base cve_2010_0426_base cve_2015_5602_base \
	blank_ubuntu_20 blank_ubuntu_22 pengine_exploit_base rm_kali_base rm_ubuntu_20_base rm_ubuntu_22_base \
	rm_ubuntu_14_base rm_ssh_base rm_samba_base \
	rm_shellshock_base rm_sql_injection_base rm_debian_10_base rm_cve_2015_3306_base rm_cve_2015_1427_base \
	rm_cve_2016_10033_base rm_cve_2010_0426_base rm_cve_2015_5602_base rm_shellshock_debian_wheezy_base \
	rm_blank_ubuntu_20 rm_blank_ubuntu_22 rm_pengine_exploit_base cve_2014_0160_base \
	rm_cve_2014_0160_base rm_ovs_base rm_ryu_base \
	rm_elk_base push_kali_base push_ubuntu_20_base push_ubuntu_22_base \
	push_ubuntu_14_base push_ssh_base push_samba_base \
	push_shellshock_base push_sql_injection_base push_debian_10_base push_cve_2015_3306_base \
	push_cve_2015_1427_base push_cve_2016_10033_base push_cve_2010_0426_base push_cve_2015_5602_base \
    push_blank_ubuntu_20 push_blank_ubuntu_22 push_pengine_exploit_base cve_2014_0160_base push_cve_2014_0160_base \
    push_ovs_base push_ryu_base push_elk_base pull_kali_base pull_ubuntu_20_base pull_ubuntu_22_base \
    push_shellshock_debian_wheezy_base \
    pull_ubuntu_14_base pull_ssh_base pull_samba_base pull_shellshock_base pull_shellshock_debian_wheezy_base \
    pull_sql_injection_base pull_debian_10_base pull_cve_2015_3306_base \
    pull_cve_2015_1427_base pull_cve_2016_10033_base pull_cve_2010_0426_base pull_cve_2015_5602_base \
    pull_blank_ubuntu_20 pull_blank_ubuntu_22 pull_pengine_exploit_base cve_2014_0160_base pull_cve_2014_0160_base \
    pull_ovs_base pull_ryu_base pull_elk_base spark_base rm_spark_base push_spark_base pull_spark_base \
    pull_web_dvwa_base push_web_dvwa_base rm_web_cvwa_base web_dvwa_base

all: build

# Targets for building all of the base images
kali_base:
	docker build . --no-cache -f ./docker_files/kali_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_kali_base:$(VERSION)

spark_base:
	docker build . --no-cache -f ./docker_files/spark_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_spark_base:$(VERSION)

ubuntu_20_base:
	docker build . --no-cache -f ./docker_files/ubuntu_20_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ubuntu_20_base:$(VERSION)

ubuntu_22_base:
	docker build . --no-cache -f ./docker_files/ubuntu_22_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ubuntu_22_base:$(VERSION)

ubuntu_14_base:
	docker build . --no-cache -f ./docker_files/ubuntu_14_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ubuntu_14_base:$(VERSION)

ssh_base:
	docker build . --no-cache -f ./docker_files/ssh_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ssh_base:$(VERSION)

samba_base:
	docker build . -f ./docker_files/samba_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_samba_base:$(VERSION)

shellshock_base:
	docker build . --no-cache -f ./docker_files/shellshock_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_shellshock_base:$(VERSION)

shellshock_debian_wheezy_base:
	docker build . --no-cache -f ./docker_files/shellshock_debian_wheezy_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_shellshock_debian_wheezy_base:$(VERSION)

sql_injection_base:
	docker build . --no-cache -f ./docker_files/sql_injection_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_sql_injection_base:$(VERSION)

debian_10_base:
	docker build . --no-cache -f ./docker_files/debian_10_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_debian_10_base:$(VERSION)

cve_2015_3306_base:
	docker build . --no-cache -f ./docker_files/cve_2015_3306_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2015_3306_base:$(VERSION)

cve_2015_1427_base:
	docker build . --no-cache -f ./docker_files/cve_2015_1427_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2015_1427_base:$(VERSION)

cve_2016_10033_base:
	docker build . --no-cache -f ./docker_files/cve_2016_10033_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2016_10033_base:$(VERSION)

cve_2010_0426_base:
	docker build . --no-cache -f ./docker_files/cve_2010_0426_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2010_0426_base:$(VERSION)

cve_2015_5602_base:
	docker build . --no-cache -f ./docker_files/cve_2015_5602_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2015_5602_base:$(VERSION)

blank_ubuntu_20:
	docker build . --no-cache -f ./docker_files/blank_ubuntu_20/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_blank_ubuntu_20:$(VERSION)

blank_ubuntu_22:
	docker build . --no-cache -f ./docker_files/blank_ubuntu_22/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_blank_ubuntu_22:$(VERSION)

pengine_exploit_base:
	docker build . --no-cache -f ./docker_files/pengine_exploit_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_pengine_exploit_base:$(VERSION)

cve_2014_0160_base:
	docker build . --no-cache -f ./docker_files/cve_2014_0160_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2014_0160_base:$(VERSION)

ovs_base:
	docker build . --no-cache -f ./docker_files/ovs_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ovs_base:$(VERSION)

ryu_base:
	docker build . --no-cache -f ./docker_files/ryu_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ryu_base:$(VERSION)

elk_base:
	docker build . --no-cache -f ./docker_files/elk_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_elk_base:$(VERSION)

web_dvwa_base:
	docker build . --no-cache -f ./docker_files/web_dvwa_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_web_dvwa_base:$(VERSION)

# Targets for removing all of the base images
rm_kali_base:
	-docker rmi $(DOCKERHUB_USER)/csle_kali_base:$(VERSION)

rm_spark_base:
	-docker rmi $(DOCKERHUB_USER)/csle_spark_base:$(VERSION)

rm_ubuntu_20_base:
	-docker rmi $(DOCKERHUB_USER)/csle_ubuntu_20_base:$(VERSION)

rm_ubuntu_22_base:
	-docker rmi $(DOCKERHUB_USER)/csle_ubuntu_22_base:$(VERSION)

rm_ubuntu_14_base:
	-docker rmi $(DOCKERHUB_USER)/csle_ubuntu_14_base:$(VERSION)

rm_ssh_base:
	-docker rmi $(DOCKERHUB_USER)/csle_ssh_base:$(VERSION)

rm_samba_base:
	-docker rmi $(DOCKERHUB_USER)/csle_samba_base:$(VERSION)

rm_shellshock_base:
	-docker rmi $(DOCKERHUB_USER)/csle_shellshock_base:$(VERSION)

rm_shellshock_debian_wheezy_base:
	-docker rmi $(DOCKERHUB_USER)/csle_shellshock_debian_wheezy_base:$(VERSION)

rm_sql_injection_base:
	-docker rmi $(DOCKERHUB_USER)/csle_sql_injection_base:$(VERSION)

rm_debian_10_base:
	-docker rmi $(DOCKERHUB_USER)/csle_debian_10_base:$(VERSION)

rm_cve_2015_3306_base:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_3306_base:$(VERSION)

rm_cve_2015_1427_base:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_1427_base:$(VERSION)

rm_cve_2016_10033_base:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2016_10033_base:$(VERSION)

rm_cve_2010_0426_base:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2010_0426_base:$(VERSION)

rm_cve_2015_5602_base:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_5602_base:$(VERSION)

rm_blank_ubuntu_20:
	-docker rmi $(DOCKERHUB_USER)/csle_blank_ubuntu_20:$(VERSION)

rm_blank_ubuntu_22:
	-docker rmi $(DOCKERHUB_USER)/csle_blank_ubuntu_22:$(VERSION)

rm_pengine_exploit_base:
	-docker rmi $(DOCKERHUB_USER)/csle_pengine_exploit_base:$(VERSION)

rm_cve_2014_0160_base:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2014_0160_base:$(VERSION)

rm_ovs_base:
	-docker rmi $(DOCKERHUB_USER)/csle_ovs_base:$(VERSION)

rm_ryu_base:
	-docker rmi $(DOCKERHUB_USER)/csle_ryu_base:$(VERSION)

rm_elk_base:
	-docker rmi $(DOCKERHUB_USER)/csle_elk_base:$(VERSION)

rm_web_dvwa_base:
	-docker rmi $(DOCKERHUB_USER)/csle_web_dvwa_base:$(VERSION)

# Targets for pushing all of the base images to DockerHub
push_kali_base:
	-docker push $(DOCKERHUB_USER)/csle_kali_base:$(VERSION)

push_spark_base:
	-docker push $(DOCKERHUB_USER)/csle_spark_base:$(VERSION)

push_ubuntu_20_base:
	-docker push $(DOCKERHUB_USER)/csle_ubuntu_20_base:$(VERSION)

push_ubuntu_22_base:
	-docker push $(DOCKERHUB_USER)/csle_ubuntu_22_base:$(VERSION)

push_ubuntu_14_base:
	-docker push $(DOCKERHUB_USER)/csle_ubuntu_14_base:$(VERSION)

push_ssh_base:
	-docker push $(DOCKERHUB_USER)/csle_ssh_base:$(VERSION)

push_samba_base:
	-docker push $(DOCKERHUB_USER)/csle_samba_base:$(VERSION)

push_shellshock_base:
	-docker push $(DOCKERHUB_USER)/csle_shellshock_base:$(VERSION)

push_shellshock_debian_wheezy_base:
	-docker push $(DOCKERHUB_USER)/csle_shellshock_debian_wheezy_base:$(VERSION)

push_sql_injection_base:
	-docker push $(DOCKERHUB_USER)/csle_sql_injection_base:$(VERSION)

push_debian_10_base:
	-docker push $(DOCKERHUB_USER)/csle_debian_10_base:$(VERSION)

push_cve_2015_3306_base:
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_3306_base:$(VERSION)

push_cve_2015_1427_base:
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_1427_base:$(VERSION)

push_cve_2016_10033_base:
	-docker push $(DOCKERHUB_USER)/csle_cve_2016_10033_base:$(VERSION)

push_cve_2010_0426_base:
	-docker push $(DOCKERHUB_USER)/csle_cve_2010_0426_base:$(VERSION)

push_cve_2015_5602_base:
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_5602_base:$(VERSION)

push_blank_ubuntu_20:
	-docker push $(DOCKERHUB_USER)/csle_blank_ubuntu_20:$(VERSION)

push_blank_ubuntu_22:
	-docker push $(DOCKERHUB_USER)/csle_blank_ubuntu_22:$(VERSION)

push_pengine_exploit_base:
	-docker push $(DOCKERHUB_USER)/csle_pengine_exploit_base:$(VERSION)

push_cve_2014_0160_base:
	-docker push $(DOCKERHUB_USER)/csle_cve_2014_0160_base:$(VERSION)

push_ovs_base:
	-docker push $(DOCKERHUB_USER)/csle_ovs_base:$(VERSION)

push_ryu_base:
	-docker push $(DOCKERHUB_USER)/csle_ryu_base:$(VERSION)

push_elk_base:
	-docker push $(DOCKERHUB_USER)/csle_elk_base:$(VERSION)

push_web_dvwa_base:
	-docker push $(DOCKERHUB_USER)/csle_web_dvwa_base:$(VERSION)

# Targets for pulling all of the base images from DockerHub
pull_kali_base:
	-docker pull $(DOCKERHUB_USER)/csle_kali_base:$(VERSION)

pull_spark_base:
	-docker pull $(DOCKERHUB_USER)/csle_spark_base:$(VERSION)

pull_ubuntu_20_base:
	-docker pull $(DOCKERHUB_USER)/csle_ubuntu_20_base:$(VERSION)

pull_ubuntu_22_base:
	-docker pull $(DOCKERHUB_USER)/csle_ubuntu_22_base:$(VERSION)

pull_ubuntu_14_base:
	-docker pull $(DOCKERHUB_USER)/csle_ubuntu_14_base:$(VERSION)

pull_ssh_base:
	-docker pull $(DOCKERHUB_USER)/csle_ssh_base:$(VERSION)

pull_samba_base:
	-docker pull $(DOCKERHUB_USER)/csle_samba_base:$(VERSION)

pull_shellshock_base:
	-docker pull $(DOCKERHUB_USER)/csle_shellshock_base:$(VERSION)

pull_shellshock_debian_wheezy_base:
	-docker pull $(DOCKERHUB_USER)/csle_shellshock_debian_wheezy_base:$(VERSION)

pull_sql_injection_base:
	-docker pull $(DOCKERHUB_USER)/csle_sql_injection_base:$(VERSION)

pull_debian_10_base:
	-docker pull $(DOCKERHUB_USER)/csle_debian_10_base:$(VERSION)

pull_cve_2015_3306_base:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_3306_base:$(VERSION)

pull_cve_2015_1427_base:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_1427_base:$(VERSION)

pull_cve_2016_10033_base:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2016_10033_base:$(VERSION)

pull_cve_2010_0426_base:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2010_0426_base:$(VERSION)

pull_cve_2015_5602_base:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_5602_base:$(VERSION)

pull_blank_ubuntu_20:
	-docker pull $(DOCKERHUB_USER)/csle_blank_ubuntu_20:$(VERSION)

pull_blank_ubuntu_22:
	-docker pull $(DOCKERHUB_USER)/csle_blank_ubuntu_22:$(VERSION)

pull_pengine_exploit_base:
	-docker pull $(DOCKERHUB_USER)/csle_pengine_exploit_base:$(VERSION)

pull_cve_2014_0160_base:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2014_0160_base:$(VERSION)

pull_ovs_base:
	-docker pull $(DOCKERHUB_USER)/csle_ovs_base:$(VERSION)

pull_ryu_base:
	-docker pull $(DOCKERHUB_USER)/csle_ryu_base:$(VERSION)

pull_elk_base:
	-docker pull $(DOCKERHUB_USER)/csle_elk_base:$(VERSION)

pull_web_dvwa_base:
	-docker pull $(DOCKERHUB_USER)/csle_web_dvwa_base:$(VERSION)

# Build all of the base images sequentially
build:
	docker build . --no-cache -f ./docker_files/kali_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_kali_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/ubuntu_20_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ubuntu_20_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/ubuntu_22_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ubuntu_22_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/ubuntu_14_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ubuntu_14_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/ssh_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ssh_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/samba_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_samba_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/shellshock_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_shellshock_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/shellshock_debian_wheezy_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_shellshock_debian_wheezy_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/web_dvwa_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_web_dvwa_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/sql_injection_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_sql_injection_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/debian_10_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_debian_10_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/cve_2015_3306_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2015_3306_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/cve_2015_1427_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2015_1427_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/cve_2016_10033_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2016_10033_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/cve_2010_0426_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2010_0426_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/cve_2015_5602_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2015_5602_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/blank_ubuntu_20/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_blank_ubuntu_20:$(VERSION)
	docker build . --no-cache -f ./docker_files/blank_ubuntu_22/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_blank_ubuntu_22:$(VERSION)
	docker build . --no-cache -f ./docker_files/pengine_exploit_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_pengine_exploit_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/cve_2014_0160_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_cve_2014_0160_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/ovs_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ovs_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/ryu_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_ryu_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/elk_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_elk_base:$(VERSION)
	docker build . --no-cache -f ./docker_files/spark_base/docker/Dockerfile -t $(DOCKERHUB_USER)/csle_spark_base:$(VERSION)

# Remove all base images
rm_image:
	-docker rmi $(DOCKERHUB_USER)/csle_kali_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ubuntu_20_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ubuntu_22_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ubuntu_14_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ssh_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_samba_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_shellshock_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_shellshock_debian_wheezy_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_web_dvwa_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_sql_injection_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_debian_10_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_3306_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_1427_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2016_10033_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2010_0426_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_5602_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_blank_ubuntu_20:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_blank_ubuntu_22:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_pengine_exploit_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2014_0160_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ovs_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ryu_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_elk_base:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_spark_base:$(VERSION)


# Push all base images
push:
	-docker push $(DOCKERHUB_USER)/csle_kali_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ubuntu_20_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ubuntu_22_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ubuntu_14_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ssh_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_samba_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_shellshock_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_shellshock_debian_wheezy_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_web_dvwa_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_sql_injection_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_debian_10_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_3306_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_1427_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2016_10033_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2010_0426_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_5602_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_blank_ubuntu_20:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_blank_ubuntu_22:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_pengine_exploit_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2014_0160_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ovs_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ryu_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_elk_base:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_spark_base:$(VERSION)


# Pull all base images
pull:
	-docker pull $(DOCKERHUB_USER)/csle_kali_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ubuntu_20_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ubuntu_22_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ubuntu_14_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ssh_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_samba_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_shellshock_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_shellshock_debian_wheezy_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_web_dvwa_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_sql_injection_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_debian_10_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_3306_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_1427_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2016_10033_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2010_0426_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_5602_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_blank_ubuntu_20:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_blank_ubuntu_22:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_pengine_exploit_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2014_0160_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ovs_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ryu_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_elk_base:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_spark_base:$(VERSION)
