all: run

.PHONY: run

# Stops the container of the logsink
stop:
	python config.py --stop

# Stops and removes the  container of the logsink
clean:
	python config.py --clean

# Starts the container of the logsink
run:
	python config.py --run

# Installs the logsink configuration in the metastore
install:
	python config.py --install

# Uninstalls the logsink configuration from the metastore
uninstall:
	python config.py --uninstall

# Applies the configuration to a running logsink
apply_config:
	python config.py --apply

# Cleans all configuration files
clean_config:
	rm -rf ./log_sink_config.json