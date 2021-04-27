all: run users topology vuln flags

.PHONY: run

topology: ./create_topology.py
	python create_topology.py

users: ./create_users.py
	python create_users.py

flags: ./create_flags.py
	python create_flags.py

vuln: ./create_vuln.py
	python create_vuln.py

clean_config:
	rm -rf ./users.json
	rm -rf ./vulnerabilities.json
	rm -rf ./flags.json
	rm -rf ./containers.json
	rm -rf ./topology.json
	rm -rf ./containers

gen_config:
	python generate_config.py


clean_fs_cache:
	python clean_fs_cache.py



apply_config: users vuln topology flags

run:
	cd containers/hacker_kali1_1/ && $(MAKE) run
	cd containers/cve_2015_1427_1_1/ && $(MAKE) run
	cd containers/sql_injection1_1/ && $(MAKE) run
	cd containers/honeypot1_1/ && $(MAKE) run
	cd containers/shellshock1_1/ && $(MAKE) run
	cd containers/ssh1_1/ && $(MAKE) run
	cd containers/router1_1/ && $(MAKE) run


stop:
	cd containers/hacker_kali1_1/ && $(MAKE) stop
	cd containers/cve_2015_1427_1_1/ && $(MAKE) stop
	cd containers/sql_injection1_1/ && $(MAKE) stop
	cd containers/honeypot1_1/ && $(MAKE) stop
	cd containers/shellshock1_1/ && $(MAKE) stop
	cd containers/ssh1_1/ && $(MAKE) stop
	cd containers/router1_1/ && $(MAKE) stop


start:
	cd containers/hacker_kali1_1/ && $(MAKE) start
	cd containers/cve_2015_1427_1_1/ && $(MAKE) start
	cd containers/sql_injection1_1/ && $(MAKE) start
	cd containers/honeypot1_1/ && $(MAKE) start
	cd containers/shellshock1_1/ && $(MAKE) start
	cd containers/ssh1_1/ && $(MAKE) start
	cd containers/router1_1/ && $(MAKE) start


clean:
	cd containers/hacker_kali1_1/ && $(MAKE) clean
	cd containers/cve_2015_1427_1_1/ && $(MAKE) clean
	cd containers/sql_injection1_1/ && $(MAKE) clean
	cd containers/honeypot1_1/ && $(MAKE) clean
	cd containers/shellshock1_1/ && $(MAKE) clean
	cd containers/ssh1_1/ && $(MAKE) clean
	cd containers/router1_1/ && $(MAKE) clean


