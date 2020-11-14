all: run users flags topology

run:
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

topology: ./create_topology.py
	python create_topology.py

users: ./create_users.py
	python create_users.py

flags: ./create_flags.py
	python create_flags.py
