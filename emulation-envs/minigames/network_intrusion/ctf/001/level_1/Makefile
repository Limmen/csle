all: run users topology vuln gen_containers_config flags traffic

.PHONY: run

run: gen_containers_config
	cd containers/router1/ && $(MAKE) run
	cd containers/ssh1/ && $(MAKE) run
	cd containers/telnet1/ && $(MAKE) run
	cd containers/honeypot1/ && $(MAKE) run
	cd containers/ftp1/ && $(MAKE) run
	cd containers/hacker_kali1/ && $(MAKE) run

stop:
	cd containers/router1/ && $(MAKE) stop
	cd containers/ssh1/ && $(MAKE) stop
	cd containers/telnet1/ && $(MAKE) stop
	cd containers/honeypot1/ && $(MAKE) stop
	cd containers/ftp1/ && $(MAKE) stop
	cd containers/hacker_kali1/ && $(MAKE) stop

start:
	cd containers/router1/ && $(MAKE) start
	cd containers/ssh1/ && $(MAKE) start
	cd containers/telnet1/ && $(MAKE) start
	cd containers/honeypot1/ && $(MAKE) start
	cd containers/ftp1/ && $(MAKE) start
	cd containers/hacker_kali1/ && $(MAKE) start
	python create_topology.py

clean:
	cd containers/router1/ && $(MAKE) clean
	cd containers/ssh1/ && $(MAKE) clean
	cd containers/telnet1/ && $(MAKE) clean
	cd containers/honeypot1/ && $(MAKE) clean
	cd containers/ftp1/ && $(MAKE) clean
	cd containers/hacker_kali1/ && $(MAKE) clean

apply_config: users vuln flags topology gen_containers_config traffic

topology: ./create_topology.py
	python create_topology.py

users: ./create_users.py
	python create_users.py

flags: ./create_flags.py
	python create_flags.py

vuln: ./create_vuln.py
	python create_vuln.py

gen_containers_config: ./gen_containers_config.py
	python gen_containers_config.py

clean_fs_cache:
	python clean_fs_cache.py

traffic: ./create_traffic_generators.py
	python create_traffic_generators.py

stop_traffic: ./stop_traffic_generators.py
	python stop_traffic_generators.py

clean_config:
	rm -rf ./users.json
	rm -rf ./vulnerabilities.json
	rm -rf ./flags.json
	rm -rf ./containers.json
	rm -rf ./topology.json
	rm -rf ./containers.json
	rm -rf ./traffic.json