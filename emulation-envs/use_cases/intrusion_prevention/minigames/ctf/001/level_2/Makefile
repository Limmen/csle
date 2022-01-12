all: run users topology vuln gen_containers_config flags traffic

# Runs all containers in the emulation
run: gen_containers_config
	cd containers/router1/ && $(MAKE) run
	cd containers/ssh1/ && $(MAKE) run
	cd containers/ssh2/ && $(MAKE) run
	cd containers/ssh3/ && $(MAKE) run
	cd containers/telnet1/ && $(MAKE) run
	cd containers/telnet2/ && $(MAKE) run
	cd containers/telnet3/ && $(MAKE) run
	cd containers/honeypot1/ && $(MAKE) run
	cd containers/honeypot2/ && $(MAKE) run
	cd containers/ftp1/ && $(MAKE) run
	cd containers/ftp2/ && $(MAKE) run
	cd containers/hacker_kali1/ && $(MAKE) run
	cd containers/client1/ && $(MAKE) run

# Stops all containers in the emulation
stop:
	cd containers/router1/ && $(MAKE) stop
	cd containers/ssh1/ && $(MAKE) stop
	cd containers/ssh2/ && $(MAKE) stop
	cd containers/ssh3/ && $(MAKE) stop
	cd containers/telnet1/ && $(MAKE) stop
	cd containers/telnet2/ && $(MAKE) stop
	cd containers/telnet3/ && $(MAKE) stop
	cd containers/honeypot1/ && $(MAKE) stop
	cd containers/honeypot2/ && $(MAKE) stop
	cd containers/ftp1/ && $(MAKE) stop
	cd containers/ftp2/ && $(MAKE) stop
	cd containers/hacker_kali1/ && $(MAKE) stop
	cd containers/client1/ && $(MAKE) stop

# Starts all containers in the emulation
start:
	cd containers/router1/ && $(MAKE) start
	cd containers/ssh1/ && $(MAKE) start
	cd containers/ssh2/ && $(MAKE) start
	cd containers/ssh3/ && $(MAKE) start
	cd containers/telnet1/ && $(MAKE) start
	cd containers/telnet2/ && $(MAKE) start
	cd containers/telnet3/ && $(MAKE) start
	cd containers/honeypot1/ && $(MAKE) start
	cd containers/honeypot2/ && $(MAKE) start
	cd containers/ftp1/ && $(MAKE) start
	cd containers/ftp2/ && $(MAKE) start
	cd containers/hacker_kali1/ && $(MAKE) start
	cd containers/client1/ && $(MAKE) start
	python create_topology.py

# Stops and removes all containers in the emulation
clean:
	cd containers/router1/ && $(MAKE) clean
	cd containers/ssh1/ && $(MAKE) clean
	cd containers/ssh2/ && $(MAKE) clean
	cd containers/ssh3/ && $(MAKE) clean
	cd containers/telnet1/ && $(MAKE) clean
	cd containers/telnet2/ && $(MAKE) clean
	cd containers/telnet3/ && $(MAKE) clean
	cd containers/honeypot1/ && $(MAKE) clean
	cd containers/honeypot2/ && $(MAKE) clean
	cd containers/ftp1/ && $(MAKE) clean
	cd containers/ftp2/ && $(MAKE) clean
	cd containers/hacker_kali1/ && $(MAKE) clean
	cd containers/client1/ && $(MAKE) clean

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