all: run users topology vuln flags

.PHONY: run

topology: create_topology.py
	python create_topology.py

users: create_users.py
	python create_users.py

flags: create_flags.py
	python create_flags.py

vuln: create_vuln.py
	python create_vuln.py

traffic: create_traffic_generators.py
	python create_traffic_generators.py

clean_config:
	rm -rf ./users.json
	rm -rf ./vulnerabilities.json
	rm -rf ./flags.json
	rm -rf ./containers.json
	rm -rf ./topology.json
	rm -rf ./traffic.json
	rm -rf ./containers

gen_config:
	python generate_config.py


clean_fs_cache:
	python clean_fs_cache.py


apply_config: users vuln topology flags

run:
	cd containers/hacker_kali1_1/ && $(MAKE) run
	cd containers/ssh2_1/ && $(MAKE) run
	cd containers/telnet2_1/ && $(MAKE) run
	cd containers/ssh1_1/ && $(MAKE) run
	cd containers/telnet1_1/ && $(MAKE) run
	cd containers/telnet1_3/ && $(MAKE) run
	cd containers/ssh2_3/ && $(MAKE) run
	cd containers/telnet3_1/ && $(MAKE) run
	cd containers/ssh3_1/ && $(MAKE) run
	cd containers/telnet2_3/ && $(MAKE) run
	cd containers/telnet3_3/ && $(MAKE) run
	cd containers/ssh2_5/ && $(MAKE) run
	cd containers/ftp1_1/ && $(MAKE) run
	cd containers/router2_1/ && $(MAKE) run


stop:
	cd containers/hacker_kali1_1/ && $(MAKE) stop
	cd containers/ssh2_1/ && $(MAKE) stop
	cd containers/telnet2_1/ && $(MAKE) stop
	cd containers/ssh1_1/ && $(MAKE) stop
	cd containers/telnet1_1/ && $(MAKE) stop
	cd containers/telnet1_3/ && $(MAKE) stop
	cd containers/ssh2_3/ && $(MAKE) stop
	cd containers/telnet3_1/ && $(MAKE) stop
	cd containers/ssh3_1/ && $(MAKE) stop
	cd containers/telnet2_3/ && $(MAKE) stop
	cd containers/telnet3_3/ && $(MAKE) stop
	cd containers/ssh2_5/ && $(MAKE) stop
	cd containers/ftp1_1/ && $(MAKE) stop
	cd containers/router2_1/ && $(MAKE) stop


start:
	cd containers/hacker_kali1_1/ && $(MAKE) start
	cd containers/ssh2_1/ && $(MAKE) start
	cd containers/telnet2_1/ && $(MAKE) start
	cd containers/ssh1_1/ && $(MAKE) start
	cd containers/telnet1_1/ && $(MAKE) start
	cd containers/telnet1_3/ && $(MAKE) start
	cd containers/ssh2_3/ && $(MAKE) start
	cd containers/telnet3_1/ && $(MAKE) start
	cd containers/ssh3_1/ && $(MAKE) start
	cd containers/telnet2_3/ && $(MAKE) start
	cd containers/telnet3_3/ && $(MAKE) start
	cd containers/ssh2_5/ && $(MAKE) start
	cd containers/ftp1_1/ && $(MAKE) start
	cd containers/router2_1/ && $(MAKE) start


clean:
	cd containers/hacker_kali1_1/ && $(MAKE) clean
	cd containers/ssh2_1/ && $(MAKE) clean
	cd containers/telnet2_1/ && $(MAKE) clean
	cd containers/ssh1_1/ && $(MAKE) clean
	cd containers/telnet1_1/ && $(MAKE) clean
	cd containers/telnet1_3/ && $(MAKE) clean
	cd containers/ssh2_3/ && $(MAKE) clean
	cd containers/telnet3_1/ && $(MAKE) clean
	cd containers/ssh3_1/ && $(MAKE) clean
	cd containers/telnet2_3/ && $(MAKE) clean
	cd containers/telnet3_3/ && $(MAKE) clean
	cd containers/ssh2_5/ && $(MAKE) clean
	cd containers/ftp1_1/ && $(MAKE) clean
	cd containers/router2_1/ && $(MAKE) clean


