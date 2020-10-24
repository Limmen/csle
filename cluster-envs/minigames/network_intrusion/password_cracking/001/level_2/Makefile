all: run

run: router ssh telnet honeypot ftp hacker_kali

router:
	cd containers/router/ && $(MAKE) build
	cd containers/router/ && $(MAKE) run

ssh:
	cd containers/ssh/ && $(MAKE) build
	cd containers/ssh/ && $(MAKE) run

telnet:
	cd containers/telnet/ && $(MAKE) build
	cd containers/telnet/ && $(MAKE) run

honeypot:
	cd containers/honeypot/ && $(MAKE) build
	cd containers/honeypot/ && $(MAKE) run

ftp:
	cd containers/ftp/ && $(MAKE) build
	cd containers/ftp/ && $(MAKE) run

hacker_kali:
	cd containers/hacker_kali/ && $(MAKE) build
	cd containers/hacker_kali/ && $(MAKE) run

net:
	cd containers/router/ && $(MAKE) net

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

rm-image:
	cd containers/router/ && $(MAKE) rm-image
	cd containers/ssh/ && $(MAKE) rm-image
	cd containers/telnet/ && $(MAKE) rm-image
	cd containers/honeypot/ && $(MAKE) rm-image
	cd containers/ftp/ && $(MAKE) rm-image
	cd containers/hacker_kali/ && $(MAKE) rm-image

build:
	cd containers/router/&& $(MAKE) build
	cd containers/ssh/ && $(MAKE) build
	cd containers/telnet/ && $(MAKE) build
	cd containers/honeypot/ && $(MAKE) build
	cd containers/ftp/ && $(MAKE) build
	cd containers/hacker_kali/ && $(MAKE) build

rm-net:
	cd containers/router/ && $(MAKE) rm-net
