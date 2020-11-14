all: run users topology flags

run:
	cd containers/router/ && $(MAKE) run
	cd containers/ssh/ && $(MAKE) run
	cd containers/telnet/ && $(MAKE) run
	cd containers/honeypot/ && $(MAKE) run
	cd containers/ftp/ && $(MAKE) run
	cd containers/hacker_kali/ && $(MAKE) run

stop:
	cd containers/router/ && $(MAKE) stop
	cd containers/ssh/ && $(MAKE) stop
	cd containers/telnet/ && $(MAKE) stop
	cd containers/honeypot/ && $(MAKE) stop
	cd containers/ftp/ && $(MAKE) stop
	cd containers/hacker_kali/ && $(MAKE) stop

start:
	cd containers/router/ && $(MAKE) start
	cd containers/ssh/ && $(MAKE) start
	cd containers/telnet/ && $(MAKE) start
	cd containers/honeypot/ && $(MAKE) start
	cd containers/ftp/ && $(MAKE) start
	cd containers/hacker_kali/ && $(MAKE) start

clean:
	cd containers/router/ && $(MAKE) clean
	cd containers/ssh/ && $(MAKE) clean
	cd containers/telnet/ && $(MAKE) clean
	cd containers/honeypot/ && $(MAKE) clean
	cd containers/ftp/ && $(MAKE) clean
	cd containers/hacker_kali/ && $(MAKE) clean

topology: ./create_topology.py
	python create_topology.py

users: ./create_users.py
	python create_users.py

flags: ./create_flags.py
	python create_flags.py