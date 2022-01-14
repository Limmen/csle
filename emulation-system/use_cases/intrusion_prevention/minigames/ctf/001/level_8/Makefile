all: run users topology vuln gen_containers_config flags resources traffic

.PHONY: run

# Runs all containers in the emulation
run: gen_containers_config
	cd containers/router_2_1/ && $(MAKE) run
	cd containers/ssh_1_1/ && $(MAKE) run
	cd containers/telnet_1_1/ && $(MAKE) run
	cd containers/honeypot_1_1/ && $(MAKE) run
	cd containers/ftp_1_1/ && $(MAKE) run
	cd containers/hacker_kali_1/ && $(MAKE) run
	cd containers/samba_1_1/ && $(MAKE) run
	cd containers/shellshock_1_1/ && $(MAKE) run
	cd containers/sql_injection_1_1/ && $(MAKE) run
	cd containers/cve_2015_3306_1_1/ && $(MAKE) run
	cd containers/cve_2015_1427_1_1/ && $(MAKE) run
	cd containers/cve_2016_10033_1_1/ && $(MAKE) run
	cd containers/cve_2010_0426_1_1/ && $(MAKE) run
	cd containers/cve_2015_5602_1_1/ && $(MAKE) run
	cd containers/ssh_1_2/ && $(MAKE) run
	cd containers/ssh_1_3/ && $(MAKE) run
	cd containers/ssh_1_4/ && $(MAKE) run
	cd containers/honeypot_1_2/ && $(MAKE) run
	cd containers/samba_1_2/ && $(MAKE) run
	cd containers/shellshock_1_2/ && $(MAKE) run
	cd containers/sql_injection_1_2/ && $(MAKE) run
	cd containers/cve_2015_3306_1_2/ && $(MAKE) run
	cd containers/cve_2015_1427_1_2/ && $(MAKE) run
	cd containers/cve_2016_10033_1_2/ && $(MAKE) run
	cd containers/cve_2010_0426_1_2/ && $(MAKE) run
	cd containers/cve_2015_5602_1_2/ && $(MAKE) run
	cd containers/client_1_1/ && $(MAKE) run

# Stops all containers in the emulation
stop:
	cd containers/router_2_1/ && $(MAKE) stop
	cd containers/ssh_1_1/ && $(MAKE) stop
	cd containers/telnet_1_1/ && $(MAKE) stop
	cd containers/honeypot_1_1/ && $(MAKE) stop
	cd containers/ftp_1_1/ && $(MAKE) stop
	cd containers/hacker_kali_1_1/ && $(MAKE) stop
	cd containers/samba_1_1/ && $(MAKE) stop
	cd containers/shellshock_1_1/ && $(MAKE) stop
	cd containers/sql_injection_1_1/ && $(MAKE) stop
	cd containers/cve_2015_3306_1_1/ && $(MAKE) stop
	cd containers/cve_2015_1427_1_1/ && $(MAKE) stop
	cd containers/cve_2016_10033_1_1/ && $(MAKE) stop
	cd containers/cve_2010_0426_1_1/ && $(MAKE) stop
	cd containers/cve_2015_5602_1_1/ && $(MAKE) stop
	cd containers/ssh_1_2/ && $(MAKE) stop
	cd containers/ssh_1_3/ && $(MAKE) stop
	cd containers/ssh_1_4/ && $(MAKE) stop
	cd containers/honeypot_1_2/ && $(MAKE) stop
	cd containers/samba_1_2/ && $(MAKE) stop
	cd containers/shellshock_1_2/ && $(MAKE) stop
	cd containers/sql_injection_1_2/ && $(MAKE) stop
	cd containers/cve_2015_3306_1_2/ && $(MAKE) stop
	cd containers/cve_2015_1427_1_2/ && $(MAKE) stop
	cd containers/cve_2016_10033_1_2/ && $(MAKE) stop
	cd containers/cve_2010_0426_1_2/ && $(MAKE) stop
	cd containers/cve_2015_5602_1_2/ && $(MAKE) stop
	cd containers/client_1_1/ && $(MAKE) stop

# Starts all containers in the emulation
start:
	cd containers/router_2_1/ && $(MAKE) start
	cd containers/ssh_1_1/ && $(MAKE) start
	cd containers/telnet_1_1/ && $(MAKE) start
	cd containers/honeypot_1_1/ && $(MAKE) start
	cd containers/ftp_1_1/ && $(MAKE) start
	cd containers/hacker_kali_1_1/ && $(MAKE) start
	cd containers/samba_1_1/ && $(MAKE) start
	cd containers/shellshock_1_1/ && $(MAKE) start
	cd containers/sql_injection_1_1/ && $(MAKE) start
	cd containers/cve_2015_3306_1_1/ && $(MAKE) start
	cd containers/cve_2015_1427_1_1/ && $(MAKE) start
	cd containers/cve_2016_10033_1_1/ && $(MAKE) start
	cd containers/cve_2010_0426_1_1/ && $(MAKE) start
	cd containers/cve_2015_5602_1_1/ && $(MAKE) start
	cd containers/ssh_1_2/ && $(MAKE) start
	cd containers/ssh_1_3/ && $(MAKE) start
	cd containers/ssh_1_4/ && $(MAKE) start
	cd containers/honeypot_1_2/ && $(MAKE) start
	cd containers/samba_1_2/ && $(MAKE) start
	cd containers/shellshock_1_2/ && $(MAKE) start
	cd containers/sql_injection_1_2/ && $(MAKE) start
	cd containers/cve_2015_3306_1_2/ && $(MAKE) start
	cd containers/cve_2015_1427_1_2/ && $(MAKE) start
	cd containers/cve_2016_10033_1_2/ && $(MAKE) start
	cd containers/cve_2010_0426_1_2/ && $(MAKE) start
	cd containers/cve_2015_5602_1_2/ && $(MAKE) start
	cd containers/client_1_1/ && $(MAKE) start
	python create_topology.py

# Stops and removes all containers in the emulation
clean:
	cd containers/router_2_1/ && $(MAKE) clean
	cd containers/ssh_1_1/ && $(MAKE) clean
	cd containers/telnet_1_1/ && $(MAKE) clean
	cd containers/honeypot_1_1/ && $(MAKE) clean
	cd containers/ftp_1_1/ && $(MAKE) clean
	cd containers/hacker_kali_1_1/ && $(MAKE) clean
	cd containers/samba_1_1/ && $(MAKE) clean
	cd containers/shellshock_1_1/ && $(MAKE) clean
	cd containers/sql_injection_1_1/ && $(MAKE) clean
	cd containers/cve_2015_3306_1_1/ && $(MAKE) clean
	cd containers/cve_2015_1427_1_1/ && $(MAKE) clean
	cd containers/cve_2016_10033_1_1/ && $(MAKE) clean
	cd containers/cve_2010_0426_1_1/ && $(MAKE) clean
	cd containers/cve_2015_5602_1_1/ && $(MAKE) clean
	cd containers/ssh_1_2/ && $(MAKE) clean
	cd containers/ssh_1_3/ && $(MAKE) clean
	cd containers/ssh_1_4/ && $(MAKE) clean
	cd containers/honeypot_1_2/ && $(MAKE) clean
	cd containers/samba_1_2/ && $(MAKE) clean
	cd containers/shellshock_1_2/ && $(MAKE) clean
	cd containers/sql_injection_1_2/ && $(MAKE) clean
	cd containers/cve_2015_3306_1_2/ && $(MAKE) clean
	cd containers/cve_2015_1427_1_2/ && $(MAKE) clean
	cd containers/cve_2016_10033_1_2/ && $(MAKE) clean
	cd containers/cve_2010_0426_1_2/ && $(MAKE) clean
	cd containers/cve_2015_5602_1_2/ && $(MAKE) clean
	cd containers/client_1_1/ && $(MAKE) clean


# Applies the config to a started emulation (assumes all containers are started)
apply_config: users vuln flags topology gen_containers_config resources traffic

# Applies the topology config to a started emulation (assumes all containers are started)
topology: create_topology.py
	python create_topology.py

# Applies the users config to a started emulation (assumes all containers are started)
users: create_users.py
	python create_users.py

# Applies the flags config to a started emulation (assumes all containers are started)
flags: create_flags.py
	python create_flags.py

# Applies the vulnerability config to a started emulation (assumes all containers are started)
vuln: create_vuln.py
	python create_vuln.py

# Generates the container configuration
gen_containers_config: gen_containers_config.py
	python gen_containers_config.py

# Applies the resource constraints config to a started emulation (assumes all containers are started)
resources: create_resource_constraints.py
	python create_resource_constraints.py

# Cleans the cache of operations in the emulation
clean_fs_cache:
	python clean_fs_cache.py

# Creates and starts the traffic generators (assume that all containers in the emulation are already started)
traffic: create_traffic_generators.py
	python create_traffic_generators.py

# Stops the traffic generators in the emulation
stop_traffic: stop_traffic_generators.py
	python stop_traffic_generators.py

# Start iperf container on the Docker host
start_iperf_container:
	docker run --name=iperf3 -d --restart=unless-stopped -p 5201:5201/tcp -p 5201:5201/udp mlabbe/iperf3

# Start iperf container on the Docker host
stop_iperf_container:
	docker stop iperf3

# Start iperf container on the Docker host
rm_iperf_container:
	docker rm iperf3

# Cleans all configuration files
clean_config:
	rm -rf ./users.json
	rm -rf ./vulnerabilities.json
	rm -rf ./flags.json
	rm -rf ./containers.json
	rm -rf ./topology.json
	rm -rf ./containers.json
	rm -rf ./traffic.json
	rm -rf ./resources.json