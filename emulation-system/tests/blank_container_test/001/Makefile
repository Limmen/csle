all: run users topology vuln gen_containers_config flags traffic

.PHONY: run

run:
	cd containers/blank_1_1/ && $(MAKE) run
	cd containers/blank_1_2/ && $(MAKE) run

stop:
	cd containers/blank_1_1/ && $(MAKE) stop
	cd containers/blank_1_2/ && $(MAKE) stop

start:
	cd containers/blank_1_1/ && $(MAKE) start
	cd containers/blank_1_2/ && $(MAKE) start

clean:
	cd containers/blank_1_1/ && $(MAKE) clean
	cd containers/blank_1_2/ && $(MAKE) clean
