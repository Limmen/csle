PROJECT=csle
VERSION=0.0.1

.PHONY: all build rm_image \
	ftp_1 ftp_2 hacker_kali_1 honeypot_1 honeypot_2 ssh_1 ssh_2 ssh_3 telnet_1 telnet_2 telnet_3 router_1 \
	router_2 samba_1 samba_2 shellshock_1 sql_injection_1 cve_2015_3306_1 cve_2015_1427_1 cve_2016_10033_1 \
	cve_2010_0426_1 cve_2015_5602_1 client_1 blank_1 pengine_exploit_1 rm_ftp_1 rm_ftp_2 rm_hacker_kali_1 \
	rm_honeypot_1 \
	rm_honeypot_2 rm_ssh_1 rm_ssh_2 rm_ssh_3 rm_telnet_1 rm_telnet_2 rm_telnet_3 rm_router_1 \
	rm_router_2 rm_samba_1 rm_samba_2 rm_shellshock_1 rm_sql_injection_1 rm_cve_2015_3306_1 rm_cve_2015_1427_1 \
	rm_cve_2016_10033_1 \
	rm_cve_2010_0426_1 rm_cve_2015_5602_1 rm_client_1 rm_blank_1 rm_pengine_exploit_1 cve_2014_0160_1 \
	rm_cve_2014_0160_1 kafka_1 ovs_1

all: build

# Targets for building all images
ftp_1:
	docker build --no-cache -f ./ftp_1/docker/Dockerfile ./ftp_1/docker/ -t $(PROJECT)/ftp_1:$(VERSION)

ftp_2:
	docker build --no-cache -f ./ftp_2/docker/Dockerfile ./ftp_2/docker/ -t $(PROJECT)/ftp_2:$(VERSION)

hacker_kali_1:
	docker build --no-cache -f ./hacker_kali_1/docker/Dockerfile ./hacker_kali_1/docker/ -t $(PROJECT)/hacker_kali_1:$(VERSION)

honeypot_1:
	docker build --no-cache -f ./honeypot_1/docker/Dockerfile ./honeypot_1/docker/ -t $(PROJECT)/honeypot_1:$(VERSION)

honeypot_2:
	docker build --no-cache -f ./honeypot_2/docker/Dockerfile ./honeypot_2/docker/ -t $(PROJECT)/honeypot_2:$(VERSION)

ssh_1:
	docker build --no-cache -f ./ssh_1/docker/Dockerfile ./ssh_1/docker/ -t $(PROJECT)/ssh_1:$(VERSION)

ssh_2:
	docker build --no-cache -f ./ssh_2/docker/Dockerfile ./ssh_2/docker/ -t $(PROJECT)/ssh_2:$(VERSION)

ssh_3:
	docker build --no-cache -f ./ssh_3/docker/Dockerfile ./ssh_3/docker/ -t $(PROJECT)/ssh_3:$(VERSION)

telnet_1:
	docker build --no-cache -f ./telnet_1/docker/Dockerfile ./telnet_1/docker/ -t $(PROJECT)/telnet_1:$(VERSION)

telnet_2:
	docker build --no-cache -f ./telnet_2/docker/Dockerfile ./telnet_2/docker/ -t $(PROJECT)/telnet_2:$(VERSION)

telnet_3:
	docker build --no-cache -f ./telnet_3/docker/Dockerfile ./telnet_3/docker/ -t $(PROJECT)/telnet_3:$(VERSION)

router_1:
	docker build --no-cache -f ./router_1/docker/Dockerfile ./router_1/docker/ -t $(PROJECT)/router_1:$(VERSION)

router_2:
	docker build --no-cache -f ./router_2/docker/Dockerfile ./router_2/docker/ -t $(PROJECT)/router_2:$(VERSION)

samba_1:
	docker build --no-cache -f ./samba_1/docker/Dockerfile ./samba_1/docker/ -t $(PROJECT)/samba_1:$(VERSION)

samba_2:
	docker build --no-cache -f ./samba_2/docker/Dockerfile ./samba_2/docker/ -t $(PROJECT)/samba_2:$(VERSION)

shellshock_1:
	docker build --no-cache -f ./shellshock_1/docker/Dockerfile ./shellshock_1/docker/ -t $(PROJECT)/shellshock_1:$(VERSION)

sql_injection_1:
	docker build --no-cache -f ./sql_injection_1/docker/Dockerfile ./sql_injection_1/docker/ -t $(PROJECT)/sql_injection_1:$(VERSION)

cve_2015_3306_1:
	docker build --no-cache -f ./cve_2015_3306_1/docker/Dockerfile ./cve_2015_3306_1/docker/ -t $(PROJECT)/cve_2015_3306_1:$(VERSION)

cve_2015_1427_1:
	docker build --no-cache -f ./cve_2015_1427_1/docker/Dockerfile ./cve_2015_1427_1/docker/ -t $(PROJECT)/cve_2015_1427_1:$(VERSION)

cve_2016_10033_1:
	docker build --no-cache -f ./cve_2016_10033_1/docker/Dockerfile ./cve_2016_10033_1/docker/ -t $(PROJECT)/cve_2016_10033_1:$(VERSION)

cve_2010_0426_1:
	docker build --no-cache -f ./cve_2010_0426_1/docker/Dockerfile ./cve_2010_0426_1/docker/ -t $(PROJECT)/cve_2010_0426_1:$(VERSION)

cve_2015_5602_1:
	docker build --no-cache -f ./cve_2015_5602_1/docker/Dockerfile ./cve_2015_5602_1/docker/ -t $(PROJECT)/cve_2015_5602_1:$(VERSION)

client_1:
	docker build --no-cache -f ./client_1/docker/Dockerfile ./client_1/docker/ -t $(PROJECT)/client_1:$(VERSION)

blank_1:
	docker build --no-cache -f ./blank_1/docker/Dockerfile ./blank_1/docker/ -t $(PROJECT)/blank_1:$(VERSION)

pengine_exploit_1:
	docker build --no-cache -f ./pengine_exploit_1/docker/Dockerfile ./pengine_exploit_1/docker/ -t $(PROJECT)/pengine_exploit_1:$(VERSION)

cve_2014_0160_1:
	docker build --no-cache -f ./cve_2014_0160_1/docker/Dockerfile ./cve_2014_0160_1/docker/ -t $(PROJECT)/cve_2014_0160_1:$(VERSION)

kafka_1:
	docker build --no-cache -f ./kafka_1/docker/Dockerfile ./kafka_1/docker/ -t $(PROJECT)/kafka_1:$(VERSION)

ovs_1:
	docker build --no-cache -f ./ovs_1/docker/Dockerfile ./ovs_1/docker/ -t $(PROJECT)/ovs_1:$(VERSION)

# Targets for removing all images

rm_ftp_1:
	-docker rmi $(PROJECT)/ftp_1:$(VERSION)

rm_ftp_2:
	-docker rmi $(PROJECT)/ftp_2:$(VERSION)

rm_hacker_kali_1:
	-docker rmi $(PROJECT)/hacker_kali_1:$(VERSION)

rm_honeypot_1:
	-docker rmi $(PROJECT)/honeypot_1:$(VERSION)

rm_honeypot_2:
	-docker rmi $(PROJECT)/honeypot_2:$(VERSION)

rm_ssh_1:
	-docker rmi $(PROJECT)/ssh_1:$(VERSION)

rm_ssh_2:
	-docker rmi $(PROJECT)/ssh_2:$(VERSION)

rm_ssh_3:
	-docker rmi $(PROJECT)/ssh_3:$(VERSION)

rm_telnet_1:
	-docker rmi $(PROJECT)/telnet_1:$(VERSION)

rm_telnet_2:
	-docker rmi $(PROJECT)/telnet_2:$(VERSION)

rm_telnet_3:
	-docker rmi $(PROJECT)/telnet_3:$(VERSION)

rm_router_1:
	-docker rmi $(PROJECT)/router_1:$(VERSION)

rm_router_2:
	-docker rmi $(PROJECT)/router_2:$(VERSION)

rm_samba_1:
	-docker rmi $(PROJECT)/samba_1:$(VERSION)

rm_samba_2:
	-docker rmi $(PROJECT)/samba_2:$(VERSION)

rm_shellshock_1:
	-docker rmi $(PROJECT)/shellshock_1:$(VERSION)

rm_sql_injection_1:
	-docker rmi $(PROJECT)/sql_injection_1:$(VERSION)

rm_cve_2015_3306_1:
	-docker rmi $(PROJECT)/cve_2015_3306_1:$(VERSION)

rm_cve_2015_1427_1:
	-docker rmi $(PROJECT)/cve_2015_1427_1:$(VERSION)

rm_cve_2016_10033_1:
	-docker rmi $(PROJECT)/cve_2016_10033_1:$(VERSION)

rm_cve_2010_0426_1:
	-docker rmi $(PROJECT)/cve_2010_0426_1:$(VERSION)

rm_cve_2015_5602_1:
	-docker rmi $(PROJECT)/cve_2015_5602_1:$(VERSION)

rm_client_1:
	-docker rmi $(PROJECT)/client_1:$(VERSION)

rm_blank_1:
	-docker rmi $(PROJECT)/blank_1:$(VERSION)

rm_pengine_exploit_1:
	-docker rmi $(PROJECT)/pengine_exploit_1:$(VERSION)

rm_cve_2014_0160_1:
	-docker rmi $(PROJECT)/cve_2014_0160_1:$(VERSION)

rm_kafka_1:
	-docker rmi $(PROJECT)/kafka_1:$(VERSION)

rm_ovs_1:
	-docker rmi $(PROJECT)/ovs_1:$(VERSION)

# Building all images sequentially
build:
	docker build --no-cache -f ./ftp_1/docker/Dockerfile ./ftp_1/docker/ -t $(PROJECT)/ftp_1:$(VERSION)
	docker build --no-cache -f ./ftp_2/docker/Dockerfile ./ftp_2/docker/ -t $(PROJECT)/ftp_2:$(VERSION)
	docker build --no-cache -f ./hacker_kali_1/docker/Dockerfile ./hacker_kali_1/docker/ -t $(PROJECT)/hacker_kali_1:$(VERSION)
	docker build --no-cache -f ./honeypot_1/docker/Dockerfile ./honeypot_1/docker/ -t $(PROJECT)/honeypot_1:$(VERSION)
	docker build --no-cache -f ./honeypot_2/docker/Dockerfile ./honeypot_2/docker/ -t $(PROJECT)/honeypot_2:$(VERSION)
	docker build --no-cache -f ./ssh_1/docker/Dockerfile ./ssh_1/docker/ -t $(PROJECT)/ssh_1:$(VERSION)
	docker build --no-cache -f ./ssh_2/docker/Dockerfile ./ssh_2/docker/ -t $(PROJECT)/ssh_2:$(VERSION)
	docker build --no-cache -f ./ssh_3/docker/Dockerfile ./ssh_3/docker/ -t $(PROJECT)/ssh_3:$(VERSION)
	docker build --no-cache -f ./telnet_1/docker/Dockerfile ./telnet_1/docker/ -t $(PROJECT)/telnet_1:$(VERSION)
	docker build --no-cache -f ./telnet_2/docker/Dockerfile ./telnet_2/docker/ -t $(PROJECT)/telnet_2:$(VERSION)
	docker build --no-cache -f ./telnet_3/docker/Dockerfile ./telnet_3/docker/ -t $(PROJECT)/telnet_3:$(VERSION)
	docker build --no-cache -f ./router_1/docker/Dockerfile ./router_1/docker/ -t $(PROJECT)/router_1:$(VERSION)
	docker build --no-cache -f ./router_2/docker/Dockerfile ./router_2/docker/ -t $(PROJECT)/router_2:$(VERSION)
	docker build --no-cache -f ./samba_1/docker/Dockerfile ./samba_1/docker/ -t $(PROJECT)/samba_1:$(VERSION)
	docker build --no-cache -f ./samba_2/docker/Dockerfile ./samba_2/docker/ -t $(PROJECT)/samba_2:$(VERSION)
	docker build --no-cache -f ./shellshock_1/docker/Dockerfile ./shellshock_1/docker/ -t $(PROJECT)/shellshock_1:$(VERSION)
	docker build --no-cache -f ./sql_injection_1/docker/Dockerfile ./sql_injection_1/docker/ -t $(PROJECT)/sql_injection_1:$(VERSION)
	docker build --no-cache -f ./cve_2015_3306_1/docker/Dockerfile ./cve_2015_3306_1/docker/ -t $(PROJECT)/cve_2015_3306_1:$(VERSION)
	docker build --no-cache -f ./cve_2015_1427_1/docker/Dockerfile ./cve_2015_1427_1/docker/ -t $(PROJECT)/cve_2015_1427_1:$(VERSION)
	docker build --no-cache -f ./cve_2016_10033_1/docker/Dockerfile ./cve_2016_10033_1/docker/ -t $(PROJECT)/cve_2016_10033_1:$(VERSION)
	docker build --no-cache -f ./cve_2010_0426_1/docker/Dockerfile ./cve_2010_0426_1/docker/ -t $(PROJECT)/cve_2010_0426_1:$(VERSION)
	docker build --no-cache -f ./cve_2015_5602_1/docker/Dockerfile ./cve_2015_5602_1/docker/ -t $(PROJECT)/cve_2015_5602_1:$(VERSION)
	docker build --no-cache -f ./client_1/docker/Dockerfile ./client_1/docker/ -t $(PROJECT)/client_1:$(VERSION)
	docker build --no-cache -f ./blank_1/docker/Dockerfile ./blank_1/docker/ -t $(PROJECT)/blank_1:$(VERSION)
	docker build --no-cache -f ./pengine_exploit_1/docker/Dockerfile ./pengine_exploit_1/docker/ -t $(PROJECT)/pengine_exploit_1:$(VERSION)
	docker build --no-cache -f ./cve_2014_0160_1/docker/Dockerfile ./cve_2014_0160_1/docker/ -t $(PROJECT)/cve_2014_0160_1:$(VERSION)
	docker build --no-cache -f ./kafka_1/docker/Dockerfile ./kafka_1/docker/ -t $(PROJECT)/kafka_1:$(VERSION)
	docker build --no-cache -f ./ovs_1/docker/Dockerfile ./ovs_1/docker/ -t $(PROJECT)/ovs_1:$(VERSION)

# Removing all images sequentially
rm_image:
	-docker rmi $(PROJECT)/ftp_1:$(VERSION)
	-docker rmi $(PROJECT)/ftp_2:$(VERSION)
	-docker rmi $(PROJECT)/hacker_kali_1:$(VERSION)
	-docker rmi $(PROJECT)/honeypot_1:$(VERSION)
	-docker rmi $(PROJECT)/honeypot_2:$(VERSION)
	-docker rmi $(PROJECT)/ssh_1:$(VERSION)
	-docker rmi $(PROJECT)/ssh_2:$(VERSION)
	-docker rmi $(PROJECT)/ssh_3:$(VERSION)
	-docker rmi $(PROJECT)/telnet_1:$(VERSION)
	-docker rmi $(PROJECT)/telnet_2:$(VERSION)
	-docker rmi $(PROJECT)/telnet_3:$(VERSION)
	-docker rmi $(PROJECT)/router_1:$(VERSION)
	-docker rmi $(PROJECT)/router_2:$(VERSION)
	-docker rmi $(PROJECT)/samba_1:$(VERSION)
	-docker rmi $(PROJECT)/samba_2:$(VERSION)
	-docker rmi $(PROJECT)/shellshock_1:$(VERSION)
	-docker rmi $(PROJECT)/sql_injection_1:$(VERSION)
	-docker rmi $(PROJECT)/cve_2015_3306_1:$(VERSION)
	-docker rmi $(PROJECT)/cve_2015_1427_1:$(VERSION)
	-docker rmi $(PROJECT)/cve_2016_10033_1:$(VERSION)
	-docker rmi $(PROJECT)/cve_2010_0426_1:$(VERSION)
	-docker rmi $(PROJECT)/cve_2015_5602_1:$(VERSION)
	-docker rmi $(PROJECT)/client_1:$(VERSION)
	-docker rmi $(PROJECT)/blank_1:$(VERSION)
	-docker rmi $(PROJECT)/pengine_exploit_1:$(VERSION)
	-docker rmi $(PROJECT)/cve_2014_0160_1:$(VERSION)
	-docker rmi $(PROJECT)/kafka_1:$(VERSION)
	-docker rmi $(PROJECT)/ovs_1:$(VERSION)