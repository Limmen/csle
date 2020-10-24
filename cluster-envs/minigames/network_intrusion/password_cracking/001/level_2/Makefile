all: run

run: router ssh1 ssh2 ssh3 telnet1 telnet2 honeypot1 ftp1 hacker_kali

router:
	cd containers/router/ && $(MAKE) build
	cd containers/router/ && $(MAKE) run

ssh1:
	cd containers/ssh1/ && $(MAKE) build
	cd containers/ssh1/ && $(MAKE) run

ssh2:
	cd containers/ssh2/ && $(MAKE) build
	cd containers/ssh2/ && $(MAKE) run

ssh3:
	cd containers/ssh3/ && $(MAKE) build
	cd containers/ssh3/ && $(MAKE) run

telnet1:
	cd containers/telnet1/ && $(MAKE) build
	cd containers/telnet1/ && $(MAKE) run

telnet2:
	cd containers/telnet1/ && $(MAKE) build
	cd containers/telnet1/ && $(MAKE) run

honeypot1:
	cd containers/honeypot1/ && $(MAKE) build
	cd containers/honeypot1/ && $(MAKE) run

ftp1:
	cd containers/ftp1/ && $(MAKE) build
	cd containers/ftp1/ && $(MAKE) run

hacker_kali:
	cd containers/hacker_kali/ && $(MAKE) build
	cd containers/hacker_kali/ && $(MAKE) run

net:
	cd containers/router/ && $(MAKE) net

stop:
	cd containers/router/ && $(MAKE) stop
	cd containers/ssh1/ && $(MAKE) stop
	cd containers/ssh2/ && $(MAKE) stop
	cd containers/ssh3/ && $(MAKE) stop
	cd containers/telnet1/ && $(MAKE) stop
	cd containers/telnet2/ && $(MAKE) stop
	cd containers/honeypot1/ && $(MAKE) stop
	cd containers/ftp1/ && $(MAKE) stop
	cd containers/hacker_kali/ && $(MAKE) stop

start:
	cd containers/router/ && $(MAKE) start
	cd containers/ssh1/ && $(MAKE) start
	cd containers/ssh2/ && $(MAKE) start
	cd containers/ssh3/ && $(MAKE) start
	cd containers/telnet1/ && $(MAKE) start
	cd containers/telnet2/ && $(MAKE) start
	cd containers/honeypot1/ && $(MAKE) start
	cd containers/ftp1/ && $(MAKE) start
	cd containers/hacker_kali/ && $(MAKE) start

clean:
	cd containers/router/ && $(MAKE) clean
	cd containers/ssh1/ && $(MAKE) clean
	cd containers/ssh2/ && $(MAKE) clean
	cd containers/ssh3/ && $(MAKE) clean
	cd containers/telnet1/ && $(MAKE) clean
	cd containers/telnet2/ && $(MAKE) clean
	cd containers/honeypot1/ && $(MAKE) clean
	cd containers/ftp1/ && $(MAKE) clean
	cd containers/hacker_kali/ && $(MAKE) clean

rm-image:
	cd containers/router/ && $(MAKE) rm-image
	cd containers/ssh1/ && $(MAKE) rm-image
	cd containers/ssh2/ && $(MAKE) rm-image
	cd containers/ssh3/ && $(MAKE) rm-image
	cd containers/telnet1/ && $(MAKE) rm-image
	cd containers/telnet2/ && $(MAKE) rm-image
	cd containers/honeypot1/ && $(MAKE) rm-image
	cd containers/ftp1/ && $(MAKE) rm-image
	cd containers/hacker_kali/ && $(MAKE) rm-image

build:
	cd containers/router/&& $(MAKE) build
	cd containers/ssh1/ && $(MAKE) build
	cd containers/ssh2/ && $(MAKE) build
	cd containers/ssh3/ && $(MAKE) build
	cd containers/telnet1/ && $(MAKE) build
	cd containers/telnet2/ && $(MAKE) build
	cd containers/honeypot1/ && $(MAKE) build
	cd containers/ftp1/ && $(MAKE) build
	cd containers/hacker_kali/ && $(MAKE) build

rm-net:
	cd containers/router/ && $(MAKE) rm-net
