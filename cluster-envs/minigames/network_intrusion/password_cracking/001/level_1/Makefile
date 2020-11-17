all: run users topology flags

.PHONY: run

run:
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

topology: ./create_topology.py
	python create_topology.py

users: ./create_users.py
	python create_users.py

flags: ./create_flags.py
	python create_flags.py