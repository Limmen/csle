all: run

run: router ssh telnet

router:
	cd containers/router/ && $(MAKE) build
	cd containers/router/ && $(MAKE) run

ssh:
	cd containers/ssh/ && $(MAKE) build
	cd containers/ssh/ && $(MAKE) run

telnet:
	cd containers/telnet/ && $(MAKE) build
	cd containers/telnet/ && $(MAKE) run

net:
	cd containers/router/ && $(MAKE) net

clean:
	cd containers/router/ && $(MAKE) clean
	cd containers/ssh/ && $(MAKE) clean
	cd containers/telnet/ && $(MAKE) clean

rm-image:
	cd containers/router/ && $(MAKE) rm-image
	cd containers/ssh/ && $(MAKE) rm-image
	cd containers/telnet/ && $(MAKE) rm-image

rm-net:
	cd containers/router/ && $(MAKE) rm-net
