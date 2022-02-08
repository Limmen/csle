all: run users topology vuln flags gen_containers_config resources traffic

.PHONY: run

# Runs all containers in the emulation
run:
	cd containers/hacker_kali_1_1/ && $(MAKE) run
	cd containers/telnet_1_1/ && $(MAKE) run
	cd containers/cve_2015_3306_1_1/ && $(MAKE) run
	cd containers/ftp_2_1/ && $(MAKE) run
	cd containers/ssh_3_1/ && $(MAKE) run
	cd containers/router_1_1/ && $(MAKE) run

# Stops all containers in the emulation
stop:
	cd containers/hacker_kali_1_1/ && $(MAKE) stop
	cd containers/telnet_1_1/ && $(MAKE) stop
	cd containers/cve_2015_3306_1_1/ && $(MAKE) stop
	cd containers/ftp_2_1/ && $(MAKE) stop
	cd containers/ssh_3_1/ && $(MAKE) stop
	cd containers/router_1_1/ && $(MAKE) stop


# Starts all containers in the emulation
start:
	cd containers/hacker_kali_1_1/ && $(MAKE) start
	cd containers/telnet_1_1/ && $(MAKE) start
	cd containers/cve_2015_3306_1_1/ && $(MAKE) start
	cd containers/ftp_2_1/ && $(MAKE) start
	cd containers/ssh_3_1/ && $(MAKE) start
	cd containers/router_1_1/ && $(MAKE) start

# Stops and removes all containers in the emulation
clean:
	cd containers/hacker_kali_1_1/ && $(MAKE) clean
	cd containers/telnet_1_1/ && $(MAKE) clean
	cd containers/cve_2015_3306_1_1/ && $(MAKE) clean
	cd containers/ftp_2_1/ && $(MAKE) clean
	cd containers/ssh_3_1/ && $(MAKE) clean
	cd containers/router_1_1/ && $(MAKE) clean


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