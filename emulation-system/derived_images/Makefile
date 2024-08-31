DOCKERHUB_USER=kimham
VERSION=0.7.0

.PHONY: all build rm_image \
	ftp_1 ftp_2 hacker_kali_1 honeypot_1 honeypot_2 ssh_1 ssh_2 ssh_3 telnet_1 telnet_2 telnet_3 router_1 \
	router_2 samba_1 samba_2 shellshock_1 sql_injection_1 cve_2015_3306_1 cve_2015_1427_1 cve_2016_10033_1 \
	cve_2010_0426_1 cve_2015_5602_1 client_1 blank_1 blank_2 pengine_exploit_1 \
	rm_ftp_1 rm_ftp_2 rm_hacker_kali_1 \
	rm_honeypot_1 \
	rm_honeypot_2 rm_ssh_1 rm_ssh_2 rm_ssh_3 rm_telnet_1 rm_telnet_2 rm_telnet_3 rm_router_1 \
	rm_router_2 rm_samba_1 rm_samba_2 rm_shellshock_1 rm_sql_injection_1 rm_cve_2015_3306_1 rm_cve_2015_1427_1 \
	rm_cve_2016_10033_1 \
	rm_cve_2010_0426_1 rm_cve_2015_5602_1 rm_client_1 rm_blank_1 rm_blank_2 rm_pengine_exploit_1 cve_2014_0160_1 \
	rm_cve_2014_0160_1 kafka_1 ovs_1 ryu_1 elk_1 rm_kafka_1 rm_ovs_1 rm_ryu_1 rm_elk_1 \
	push_ftp_1 push_ftp_2 push_hacker_kali_1 push_honeypot_1 push_honeypot_2 push_ssh_1 push_ssh_2 \
	push_ssh_3 push_telnet_1 \
	push_telnet_2 push_telnet_3 push_router_1 push_router_2 push_samba_1 push_samba_2 push_shellshock_1 \
	push_sql_injection_1 \
	push_cve_2015_3306_1 push_cve_2015_1427_1 push_cve_2016_10033_1 push_cve_2010_0426_1 \
    push_cve_2015_5602_1 push_client_1 \
    push_blank_1 push_blank_2 push_pengine_exploit_1 cve_2014_0160_1 push_cve_2014_0160_1 \
    push_kafka_1 push_ovs_1 push_ryu_1 \
    push_elk_1 \
    pull_ftp_1 pull_ftp_2 pull_hacker_kali_1 pull_honeypot_1 pull_honeypot_2 pull_ssh_1 pull_ssh_2 \
    pull_ssh_3 pull_telnet_1 \
    pull_telnet_2 pull_telnet_3 pull_router_1 pull_router_2 pull_samba_1 pull_samba_2 pull_shellshock_1 \
    pull_sql_injection_1 \
    pull_cve_2015_3306_1 pull_cve_2015_1427_1 pull_cve_2016_10033_1 pull_cve_2010_0426_1 \
    pull_cve_2015_5602_1 pull_client_1 \
    pull_blank_1 pull_blank_2 pull_pengine_exploit_1 cve_2014_0160_1 pull_cve_2014_0160_1 \
    pull_kafka_1 pull_ovs_1 pull_ryu_1 \
    pull_elk_1 spark_1 rm_spark_1 push_spark_1 pull_spark_1

all: build

# Targets for building all images
ftp_1:
	docker build --no-cache -f ./ftp_1/docker/Dockerfile ./ftp_1/docker/ -t $(DOCKERHUB_USER)/csle_ftp_1:$(VERSION)

ftp_2:
	docker build --no-cache -f ./ftp_2/docker/Dockerfile ./ftp_2/docker/ -t $(DOCKERHUB_USER)/csle_ftp_2:$(VERSION)

hacker_kali_1:
	docker build --no-cache -f ./hacker_kali_1/docker/Dockerfile ./hacker_kali_1/docker/ -t $(DOCKERHUB_USER)/csle_hacker_kali_1:$(VERSION)

honeypot_1:
	docker build --no-cache -f ./honeypot_1/docker/Dockerfile ./honeypot_1/docker/ -t $(DOCKERHUB_USER)/csle_honeypot_1:$(VERSION)

honeypot_2:
	docker build --no-cache -f ./honeypot_2/docker/Dockerfile ./honeypot_2/docker/ -t $(DOCKERHUB_USER)/csle_honeypot_2:$(VERSION)

ssh_1:
	docker build --no-cache -f ./ssh_1/docker/Dockerfile ./ssh_1/docker/ -t $(DOCKERHUB_USER)/csle_ssh_1:$(VERSION)

ssh_2:
	docker build --no-cache -f ./ssh_2/docker/Dockerfile ./ssh_2/docker/ -t $(DOCKERHUB_USER)/csle_ssh_2:$(VERSION)

ssh_3:
	docker build --no-cache -f ./ssh_3/docker/Dockerfile ./ssh_3/docker/ -t $(DOCKERHUB_USER)/csle_ssh_3:$(VERSION)

telnet_1:
	docker build --no-cache -f ./telnet_1/docker/Dockerfile ./telnet_1/docker/ -t $(DOCKERHUB_USER)/csle_telnet_1:$(VERSION)

telnet_2:
	docker build --no-cache -f ./telnet_2/docker/Dockerfile ./telnet_2/docker/ -t $(DOCKERHUB_USER)/csle_telnet_2:$(VERSION)

telnet_3:
	docker build --no-cache -f ./telnet_3/docker/Dockerfile ./telnet_3/docker/ -t $(DOCKERHUB_USER)/csle_telnet_3:$(VERSION)

router_1:
	docker build --no-cache -f ./router_1/docker/Dockerfile ./router_1/docker/ -t $(DOCKERHUB_USER)/csle_router_1:$(VERSION)

router_2:
	docker build --no-cache -f ./router_2/docker/Dockerfile ./router_2/docker/ -t $(DOCKERHUB_USER)/csle_router_2:$(VERSION)

samba_1:
	docker build --no-cache -f ./samba_1/docker/Dockerfile ./samba_1/docker/ -t $(DOCKERHUB_USER)/csle_samba_1:$(VERSION)

samba_2:
	docker build --no-cache -f ./samba_2/docker/Dockerfile ./samba_2/docker/ -t $(DOCKERHUB_USER)/csle_samba_2:$(VERSION)

shellshock_1:
	docker build --no-cache -f ./shellshock_1/docker/Dockerfile ./shellshock_1/docker/ -t $(DOCKERHUB_USER)/csle_shellshock_1:$(VERSION)

sql_injection_1:
	docker build --no-cache -f ./sql_injection_1/docker/Dockerfile ./sql_injection_1/docker/ -t $(DOCKERHUB_USER)/csle_sql_injection_1:$(VERSION)

cve_2015_3306_1:
	docker build --no-cache -f ./cve_2015_3306_1/docker/Dockerfile ./cve_2015_3306_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2015_3306_1:$(VERSION)

cve_2015_1427_1:
	docker build --no-cache -f ./cve_2015_1427_1/docker/Dockerfile ./cve_2015_1427_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2015_1427_1:$(VERSION)

cve_2016_10033_1:
	docker build --no-cache -f ./cve_2016_10033_1/docker/Dockerfile ./cve_2016_10033_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2016_10033_1:$(VERSION)

cve_2010_0426_1:
	docker build --no-cache -f ./cve_2010_0426_1/docker/Dockerfile ./cve_2010_0426_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2010_0426_1:$(VERSION)

cve_2015_5602_1:
	docker build --no-cache -f ./cve_2015_5602_1/docker/Dockerfile ./cve_2015_5602_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2015_5602_1:$(VERSION)

client_1:
	docker build --no-cache -f ./client_1/docker/Dockerfile ./client_1/docker/ -t $(DOCKERHUB_USER)/csle_client_1:$(VERSION)

blank_1:
	docker build --no-cache -f ./blank_1/docker/Dockerfile ./blank_1/docker/ -t $(DOCKERHUB_USER)/csle_blank_1:$(VERSION)

blank_2:
	docker build --no-cache -f ./blank_2/docker/Dockerfile ./blank_2/docker/ -t $(DOCKERHUB_USER)/csle_blank_2:$(VERSION)

pengine_exploit_1:
	docker build --no-cache -f ./pengine_exploit_1/docker/Dockerfile ./pengine_exploit_1/docker/ -t $(DOCKERHUB_USER)/csle_pengine_exploit_1:$(VERSION)

cve_2014_0160_1:
	docker build --no-cache -f ./cve_2014_0160_1/docker/Dockerfile ./cve_2014_0160_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2014_0160_1:$(VERSION)

kafka_1:
	docker build --no-cache -f ./kafka_1/docker/Dockerfile ./kafka_1/docker/ -t $(DOCKERHUB_USER)/csle_kafka_1:$(VERSION)

ovs_1:
	docker build --no-cache -f ./ovs_1/docker/Dockerfile ./ovs_1/docker/ -t $(DOCKERHUB_USER)/csle_ovs_1:$(VERSION)

spark_1:
	docker build --no-cache -f ./spark_1/docker/Dockerfile ./spark_1/docker/ -t $(DOCKERHUB_USER)/csle_spark_1:$(VERSION)

ryu_1:
	docker build --no-cache -f ./ryu_1/docker/Dockerfile ./ryu_1/docker/ -t $(DOCKERHUB_USER)/csle_ryu_1:$(VERSION)

elk_1:
	docker build --no-cache -f ./elk_1/docker/Dockerfile ./elk_1/docker/ -t $(DOCKERHUB_USER)/csle_elk_1:$(VERSION)

# Targets for removing all images

rm_ftp_1:
	-docker rmi $(DOCKERHUB_USER)/csle_ftp_1:$(VERSION)

rm_ftp_2:
	-docker rmi $(DOCKERHUB_USER)/csle_ftp_2:$(VERSION)

rm_hacker_kali_1:
	-docker rmi $(DOCKERHUB_USER)/csle_hacker_kali_1:$(VERSION)

rm_honeypot_1:
	-docker rmi $(DOCKERHUB_USER)/csle_honeypot_1:$(VERSION)

rm_honeypot_2:
	-docker rmi $(DOCKERHUB_USER)/csle_honeypot_2:$(VERSION)

rm_ssh_1:
	-docker rmi $(DOCKERHUB_USER)/csle_ssh_1:$(VERSION)

rm_ssh_2:
	-docker rmi $(DOCKERHUB_USER)/csle_ssh_2:$(VERSION)

rm_ssh_3:
	-docker rmi $(DOCKERHUB_USER)/csle_ssh_3:$(VERSION)

rm_telnet_1:
	-docker rmi $(DOCKERHUB_USER)/csle_telnet_1:$(VERSION)

rm_telnet_2:
	-docker rmi $(DOCKERHUB_USER)/csle_telnet_2:$(VERSION)

rm_telnet_3:
	-docker rmi $(DOCKERHUB_USER)/csle_telnet_3:$(VERSION)

rm_router_1:
	-docker rmi $(DOCKERHUB_USER)/csle_router_1:$(VERSION)

rm_router_2:
	-docker rmi $(DOCKERHUB_USER)/csle_router_2:$(VERSION)

rm_samba_1:
	-docker rmi $(DOCKERHUB_USER)/csle_samba_1:$(VERSION)

rm_samba_2:
	-docker rmi $(DOCKERHUB_USER)/csle_samba_2:$(VERSION)

rm_shellshock_1:
	-docker rmi $(DOCKERHUB_USER)/csle_shellshock_1:$(VERSION)

rm_sql_injection_1:
	-docker rmi $(DOCKERHUB_USER)/csle_sql_injection_1:$(VERSION)

rm_cve_2015_3306_1:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_3306_1:$(VERSION)

rm_cve_2015_1427_1:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_1427_1:$(VERSION)

rm_cve_2016_10033_1:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2016_10033_1:$(VERSION)

rm_cve_2010_0426_1:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2010_0426_1:$(VERSION)

rm_cve_2015_5602_1:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_5602_1:$(VERSION)

rm_client_1:
	-docker rmi $(DOCKERHUB_USER)/csle_client_1:$(VERSION)

rm_blank_1:
	-docker rmi $(DOCKERHUB_USER)/csle_blank_1:$(VERSION)

rm_blank_2:
	-docker rmi $(DOCKERHUB_USER)/csle_blank_2:$(VERSION)

rm_pengine_exploit_1:
	-docker rmi $(DOCKERHUB_USER)/csle_pengine_exploit_1:$(VERSION)

rm_cve_2014_0160_1:
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2014_0160_1:$(VERSION)

rm_kafka_1:
	-docker rmi $(DOCKERHUB_USER)/csle_kafka_1:$(VERSION)

rm_ovs_1:
	-docker rmi $(DOCKERHUB_USER)/csle_ovs_1:$(VERSION)

rm_spark_1:
	-docker rmi $(DOCKERHUB_USER)/csle_spark_1:$(VERSION)

rm_ryu_1:
	-docker rmi $(DOCKERHUB_USER)/csle_ryu_1:$(VERSION)

rm_elk_1:
	-docker rmi $(DOCKERHUB_USER)/csle_elk_1:$(VERSION)


# Targets for pushing all images

push_ftp_1:
	-docker push $(DOCKERHUB_USER)/csle_ftp_1:$(VERSION)

push_ftp_2:
	-docker push $(DOCKERHUB_USER)/csle_ftp_2:$(VERSION)

push_hacker_kali_1:
	-docker push $(DOCKERHUB_USER)/csle_hacker_kali_1:$(VERSION)

push_honeypot_1:
	-docker push $(DOCKERHUB_USER)/csle_honeypot_1:$(VERSION)

push_honeypot_2:
	-docker push $(DOCKERHUB_USER)/csle_honeypot_2:$(VERSION)

push_ssh_1:
	-docker push $(DOCKERHUB_USER)/csle_ssh_1:$(VERSION)

push_ssh_2:
	-docker push $(DOCKERHUB_USER)/csle_ssh_2:$(VERSION)

push_ssh_3:
	-docker push $(DOCKERHUB_USER)/csle_ssh_3:$(VERSION)

push_telnet_1:
	-docker push $(DOCKERHUB_USER)/csle_telnet_1:$(VERSION)

push_telnet_2:
	-docker push $(DOCKERHUB_USER)/csle_telnet_2:$(VERSION)

push_telnet_3:
	-docker push $(DOCKERHUB_USER)/csle_telnet_3:$(VERSION)

push_router_1:
	-docker push $(DOCKERHUB_USER)/csle_router_1:$(VERSION)

push_router_2:
	-docker push $(DOCKERHUB_USER)/csle_router_2:$(VERSION)

push_samba_1:
	-docker push $(DOCKERHUB_USER)/csle_samba_1:$(VERSION)

push_samba_2:
	-docker push $(DOCKERHUB_USER)/csle_samba_2:$(VERSION)

push_shellshock_1:
	-docker push $(DOCKERHUB_USER)/csle_shellshock_1:$(VERSION)

push_sql_injection_1:
	-docker push $(DOCKERHUB_USER)/csle_sql_injection_1:$(VERSION)

push_cve_2015_3306_1:
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_3306_1:$(VERSION)

push_cve_2015_1427_1:
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_1427_1:$(VERSION)

push_cve_2016_10033_1:
	-docker push $(DOCKERHUB_USER)/csle_cve_2016_10033_1:$(VERSION)

push_cve_2010_0426_1:
	-docker push $(DOCKERHUB_USER)/csle_cve_2010_0426_1:$(VERSION)

push_cve_2015_5602_1:
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_5602_1:$(VERSION)

push_client_1:
	-docker push $(DOCKERHUB_USER)/csle_client_1:$(VERSION)

push_blank_1:
	-docker push $(DOCKERHUB_USER)/csle_blank_1:$(VERSION)

push_blank_2:
	-docker push $(DOCKERHUB_USER)/csle_blank_2:$(VERSION)

push_pengine_exploit_1:
	-docker push $(DOCKERHUB_USER)/csle_pengine_exploit_1:$(VERSION)

push_cve_2014_0160_1:
	-docker push $(DOCKERHUB_USER)/csle_cve_2014_0160_1:$(VERSION)

push_kafka_1:
	-docker push $(DOCKERHUB_USER)/csle_kafka_1:$(VERSION)

push_ovs_1:
	-docker push $(DOCKERHUB_USER)/csle_ovs_1:$(VERSION)

push_spark_1:
	-docker push $(DOCKERHUB_USER)/csle_spark_1:$(VERSION)

push_ryu_1:
	-docker push $(DOCKERHUB_USER)/csle_ryu_1:$(VERSION)

push_elk_1:
	-docker push $(DOCKERHUB_USER)/csle_elk_1:$(VERSION)


# Targets for pulling all images

pull_ftp_1:
	-docker pull $(DOCKERHUB_USER)/csle_ftp_1:$(VERSION)

pull_ftp_2:
	-docker pull $(DOCKERHUB_USER)/csle_ftp_2:$(VERSION)

pull_hacker_kali_1:
	-docker pull $(DOCKERHUB_USER)/csle_hacker_kali_1:$(VERSION)

pull_honeypot_1:
	-docker pull $(DOCKERHUB_USER)/csle_honeypot_1:$(VERSION)

pull_honeypot_2:
	-docker pull $(DOCKERHUB_USER)/csle_honeypot_2:$(VERSION)

pull_ssh_1:
	-docker pull $(DOCKERHUB_USER)/csle_ssh_1:$(VERSION)

pull_ssh_2:
	-docker pull $(DOCKERHUB_USER)/csle_ssh_2:$(VERSION)

pull_ssh_3:
	-docker pull $(DOCKERHUB_USER)/csle_ssh_3:$(VERSION)

pull_telnet_1:
	-docker pull $(DOCKERHUB_USER)/csle_telnet_1:$(VERSION)

pull_telnet_2:
	-docker pull $(DOCKERHUB_USER)/csle_telnet_2:$(VERSION)

pull_telnet_3:
	-docker pull $(DOCKERHUB_USER)/csle_telnet_3:$(VERSION)

pull_router_1:
	-docker pull $(DOCKERHUB_USER)/csle_router_1:$(VERSION)

pull_router_2:
	-docker pull $(DOCKERHUB_USER)/csle_router_2:$(VERSION)

pull_samba_1:
	-docker pull $(DOCKERHUB_USER)/csle_samba_1:$(VERSION)

pull_samba_2:
	-docker pull $(DOCKERHUB_USER)/csle_samba_2:$(VERSION)

pull_shellshock_1:
	-docker pull $(DOCKERHUB_USER)/csle_shellshock_1:$(VERSION)

pull_sql_injection_1:
	-docker pull $(DOCKERHUB_USER)/csle_sql_injection_1:$(VERSION)

pull_cve_2015_3306_1:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_3306_1:$(VERSION)

pull_cve_2015_1427_1:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_1427_1:$(VERSION)

pull_cve_2016_10033_1:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2016_10033_1:$(VERSION)

pull_cve_2010_0426_1:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2010_0426_1:$(VERSION)

pull_cve_2015_5602_1:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_5602_1:$(VERSION)

pull_client_1:
	-docker pull $(DOCKERHUB_USER)/csle_client_1:$(VERSION)

pull_blank_1:
	-docker pull $(DOCKERHUB_USER)/csle_blank_1:$(VERSION)

pull_blank_2:
	-docker pull $(DOCKERHUB_USER)/csle_blank_2:$(VERSION)

pull_pengine_exploit_1:
	-docker pull $(DOCKERHUB_USER)/csle_pengine_exploit_1:$(VERSION)

pull_cve_2014_0160_1:
	-docker pull $(DOCKERHUB_USER)/csle_cve_2014_0160_1:$(VERSION)

pull_kafka_1:
	-docker pull $(DOCKERHUB_USER)/csle_kafka_1:$(VERSION)

pull_ovs_1:
	-docker pull $(DOCKERHUB_USER)/csle_ovs_1:$(VERSION)

pull_spark_1:
	-docker pull $(DOCKERHUB_USER)/csle_spark_1:$(VERSION)

pull_ryu_1:
	-docker pull $(DOCKERHUB_USER)/csle_ryu_1:$(VERSION)

pull_elk_1:
	-docker pull $(DOCKERHUB_USER)/csle_elk_1:$(VERSION)

# Building all images sequentially
build:
	docker build --no-cache -f ./ftp_1/docker/Dockerfile ./ftp_1/docker/ -t $(DOCKERHUB_USER)/csle_ftp_1:$(VERSION)
	docker build --no-cache -f ./ftp_2/docker/Dockerfile ./ftp_2/docker/ -t $(DOCKERHUB_USER)/csle_ftp_2:$(VERSION)
	docker build --no-cache -f ./hacker_kali_1/docker/Dockerfile ./hacker_kali_1/docker/ -t $(DOCKERHUB_USER)/csle_hacker_kali_1:$(VERSION)
	docker build --no-cache -f ./honeypot_1/docker/Dockerfile ./honeypot_1/docker/ -t $(DOCKERHUB_USER)/csle_honeypot_1:$(VERSION)
	docker build --no-cache -f ./honeypot_2/docker/Dockerfile ./honeypot_2/docker/ -t $(DOCKERHUB_USER)/csle_honeypot_2:$(VERSION)
	docker build --no-cache -f ./ssh_1/docker/Dockerfile ./ssh_1/docker/ -t $(DOCKERHUB_USER)/csle_ssh_1:$(VERSION)
	docker build --no-cache -f ./ssh_2/docker/Dockerfile ./ssh_2/docker/ -t $(DOCKERHUB_USER)/csle_ssh_2:$(VERSION)
	docker build --no-cache -f ./ssh_3/docker/Dockerfile ./ssh_3/docker/ -t $(DOCKERHUB_USER)/csle_ssh_3:$(VERSION)
	docker build --no-cache -f ./telnet_1/docker/Dockerfile ./telnet_1/docker/ -t $(DOCKERHUB_USER)/csle_telnet_1:$(VERSION)
	docker build --no-cache -f ./telnet_2/docker/Dockerfile ./telnet_2/docker/ -t $(DOCKERHUB_USER)/csle_telnet_2:$(VERSION)
	docker build --no-cache -f ./telnet_3/docker/Dockerfile ./telnet_3/docker/ -t $(DOCKERHUB_USER)/csle_telnet_3:$(VERSION)
	docker build --no-cache -f ./router_1/docker/Dockerfile ./router_1/docker/ -t $(DOCKERHUB_USER)/csle_router_1:$(VERSION)
	docker build --no-cache -f ./router_2/docker/Dockerfile ./router_2/docker/ -t $(DOCKERHUB_USER)/csle_router_2:$(VERSION)
	docker build --no-cache -f ./samba_1/docker/Dockerfile ./samba_1/docker/ -t $(DOCKERHUB_USER)/csle_samba_1:$(VERSION)
	docker build --no-cache -f ./samba_2/docker/Dockerfile ./samba_2/docker/ -t $(DOCKERHUB_USER)/csle_samba_2:$(VERSION)
	docker build --no-cache -f ./shellshock_1/docker/Dockerfile ./shellshock_1/docker/ -t $(DOCKERHUB_USER)/csle_shellshock_1:$(VERSION)
	docker build --no-cache -f ./sql_injection_1/docker/Dockerfile ./sql_injection_1/docker/ -t $(DOCKERHUB_USER)/csle_sql_injection_1:$(VERSION)
	docker build --no-cache -f ./cve_2015_3306_1/docker/Dockerfile ./cve_2015_3306_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2015_3306_1:$(VERSION)
	docker build --no-cache -f ./cve_2015_1427_1/docker/Dockerfile ./cve_2015_1427_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2015_1427_1:$(VERSION)
	docker build --no-cache -f ./cve_2016_10033_1/docker/Dockerfile ./cve_2016_10033_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2016_10033_1:$(VERSION)
	docker build --no-cache -f ./cve_2010_0426_1/docker/Dockerfile ./cve_2010_0426_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2010_0426_1:$(VERSION)
	docker build --no-cache -f ./cve_2015_5602_1/docker/Dockerfile ./cve_2015_5602_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2015_5602_1:$(VERSION)
	docker build --no-cache -f ./client_1/docker/Dockerfile ./client_1/docker/ -t $(DOCKERHUB_USER)/csle_client_1:$(VERSION)
	docker build --no-cache -f ./blank_1/docker/Dockerfile ./blank_1/docker/ -t $(DOCKERHUB_USER)/csle_blank_1:$(VERSION)
	docker build --no-cache -f ./blank_2/docker/Dockerfile ./blank_2/docker/ -t $(DOCKERHUB_USER)/csle_blank_2:$(VERSION)
	docker build --no-cache -f ./pengine_exploit_1/docker/Dockerfile ./pengine_exploit_1/docker/ -t $(DOCKERHUB_USER)/csle_pengine_exploit_1:$(VERSION)
	docker build --no-cache -f ./cve_2014_0160_1/docker/Dockerfile ./cve_2014_0160_1/docker/ -t $(DOCKERHUB_USER)/csle_cve_2014_0160_1:$(VERSION)
	docker build --no-cache -f ./kafka_1/docker/Dockerfile ./kafka_1/docker/ -t $(DOCKERHUB_USER)/csle_kafka_1:$(VERSION)
	docker build --no-cache -f ./ovs_1/docker/Dockerfile ./ovs_1/docker/ -t $(DOCKERHUB_USER)/csle_ovs_1:$(VERSION)
	docker build --no-cache -f ./ryu_1/docker/Dockerfile ./ryu_1/docker/ -t $(DOCKERHUB_USER)/csle_ryu_1:$(VERSION)
	docker build --no-cache -f ./elk_1/docker/Dockerfile ./elk_1/docker/ -t $(DOCKERHUB_USER)/csle_elk_1:$(VERSION)
	docker build --no-cache -f ./spark_1/docker/Dockerfile ./spark_1/docker/ -t $(DOCKERHUB_USER)/csle_spark_1:$(VERSION)

# Removing all images sequentially
rm_image:
	-docker rmi $(DOCKERHUB_USER)/csle_ftp_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ftp_2:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_hacker_kali_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_honeypot_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_honeypot_2:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ssh_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ssh_2:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ssh_3:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_telnet_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_telnet_2:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_telnet_3:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_router_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_router_2:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_samba_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_samba_2:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_shellshock_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_sql_injection_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_3306_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_1427_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2016_10033_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2010_0426_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2015_5602_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_client_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_blank_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_blank_2:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_pengine_exploit_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_cve_2014_0160_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_kafka_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ovs_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_ryu_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_elk_1:$(VERSION)
	-docker rmi $(DOCKERHUB_USER)/csle_spark_1:$(VERSION)


# Pushing all images sequentially
push:
	-docker push $(DOCKERHUB_USER)/csle_ftp_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ftp_2:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_hacker_kali_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_honeypot_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_honeypot_2:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ssh_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ssh_2:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ssh_3:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_telnet_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_telnet_2:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_telnet_3:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_router_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_router_2:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_samba_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_samba_2:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_shellshock_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_sql_injection_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_3306_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_1427_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2016_10033_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2010_0426_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2015_5602_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_client_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_blank_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_blank_2:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_pengine_exploit_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_cve_2014_0160_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_kafka_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ovs_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_ryu_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_elk_1:$(VERSION)
	-docker push $(DOCKERHUB_USER)/csle_spark_1:$(VERSION)


# Pullin all images sequentially
pull:
	-docker pull $(DOCKERHUB_USER)/csle_ftp_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ftp_2:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_hacker_kali_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_honeypot_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_honeypot_2:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ssh_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ssh_2:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ssh_3:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_telnet_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_telnet_2:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_telnet_3:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_router_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_router_2:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_samba_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_samba_2:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_shellshock_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_sql_injection_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_3306_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_1427_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2016_10033_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2010_0426_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2015_5602_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_client_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_blank_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_blank_2:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_pengine_exploit_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_cve_2014_0160_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_kafka_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ovs_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_ryu_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_elk_1:$(VERSION)
	-docker pull $(DOCKERHUB_USER)/csle_spark_1:$(VERSION)