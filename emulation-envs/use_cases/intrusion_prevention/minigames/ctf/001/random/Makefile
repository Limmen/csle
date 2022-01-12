all: run users topology vuln flags

.PHONY: run

# Runs all containers in the emulation
run:
	cd containers/hacker_kali1_1/ && $(MAKE) run
	cd containers/telnet1_1/ && $(MAKE) run
	cd containers/cve_2015_3306_1_1/ && $(MAKE) run
	cd containers/ftp2_1/ && $(MAKE) run
	cd containers/ssh3_1/ && $(MAKE) run
	cd containers/router1_1/ && $(MAKE) run

# Stops all containers in the emulation
stop:
	cd containers/hacker_kali1_1/ && $(MAKE) stop
	cd containers/telnet1_1/ && $(MAKE) stop
	cd containers/cve_2015_3306_1_1/ && $(MAKE) stop
	cd containers/ftp2_1/ && $(MAKE) stop
	cd containers/ssh3_1/ && $(MAKE) stop
	cd containers/router1_1/ && $(MAKE) stop


# Starts all containers in the emulation
start:
	cd containers/hacker_kali1_1/ && $(MAKE) start
	cd containers/telnet1_1/ && $(MAKE) start
	cd containers/cve_2015_3306_1_1/ && $(MAKE) start
	cd containers/ftp2_1/ && $(MAKE) start
	cd containers/ssh3_1/ && $(MAKE) start
	cd containers/router1_1/ && $(MAKE) start

# Stops and removes all containers in the emulation
clean:
	cd containers/hacker_kali1_1/ && $(MAKE) clean
	cd containers/telnet1_1/ && $(MAKE) clean
	cd containers/cve_2015_3306_1_1/ && $(MAKE) clean
	cd containers/ftp2_1/ && $(MAKE) clean
	cd containers/ssh3_1/ && $(MAKE) clean
	cd containers/router1_1/ && $(MAKE) clean


# Applies the config to a started emulation (assumes all containers are started)
apply_config: users vuln flags topology gen_containers_config traffic

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

# Cleans the cache of operations in the emulation
clean_fs_cache:
	python clean_fs_cache.py

# Creates and starts the traffic generators (assume that all containers in the emulation are already started)
traffic: create_traffic_generators.py
	python create_traffic_generators.py

# Stops the traffoc generators in the emulation
stop_traffic: stop_traffic_generators.py
	python stop_traffic_generators.py

# Cleans all configuration files
clean_config:
	rm -rf ./users.json
	rm -rf ./vulnerabilities.json
	rm -rf ./flags.json
	rm -rf ./containers.json
	rm -rf ./topology.json
	rm -rf ./containers.json
	rm -rf ./traffic.json