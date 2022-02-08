all: run

.PHONY: run

# Stops all containers in the emulation
stop:
	python config.py --stop

# Stops and removes all containers in the emulation
clean:
	python config.py --clean

# Starts all containers in the emulation
run:
	python config.py --run

# Applies the configuration to a running emulation
apply_config:
	python config.py --apply

# Installs the configuration in the metastore
install:
	python config.py --install

# Uninstalls the configuration from the metastore
uninstall:
	python config.py --uninstall

# Cleans all configuration files
clean_config:
	rm -rf ./config.json
	rm -rf ./containers