all: run users flags topology vuln gen_containers_config

run:
	cd containers/router2/ && $(MAKE) run
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

stop:
	cd containers/router2/ && $(MAKE) stop
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

start:
	cd containers/router2/ && $(MAKE) start
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
	python create_topology.py

clean:
	cd containers/router2/ && $(MAKE) clean
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

clean_config:
	rm -rf ./users.json
	rm -rf ./vulnerabilities.json
	rm -rf ./flags.json
	rm -rf ./containers.json
	rm -rf ./topology.json
	rm -rf ./containers.json