# Installs the configuration in the metastore
install:
	python config_v_001.py --install
	python config_v_002.py --install
	python config_v_003.py --install

# Uninstalls the configuration from the metastore
uninstall:
	python config_v_001.py --uninstall
	python config_v_002.py --uninstall
	python config_v_003.py --uninstall

# Cleans all configuration files
clean_config:
	rm -rf ./config.json