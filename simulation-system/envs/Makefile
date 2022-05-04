# Targets for installing each individual env
install_stopping_game:
	cd stopping_game/ && $(MAKE) install

install_stopping_mdp_attacker:
	cd stopping_mdp_attacker/ && $(MAKE) install

install_stopping_pomdp_defender:
	cd stopping_pomdp_defender/ && $(MAKE) install

# Installs all emulations
install:
	cd stopping_game/ && $(MAKE) install
	cd stopping_mdp_attacker/ && $(MAKE) install
	cd stopping_pomdp_defender/ && $(MAKE) install

# Targets for uninstalling each individual env
uninstall_stopping_game:
	cd stopping_game/ && $(MAKE) uninstall

uninstall_stopping_mdp_attacker:
	cd stopping_mdp_attacker/ && $(MAKE) uninstall

uninstall_stopping_pomdp_defender:
	cd stopping_pomdp_defender/ && $(MAKE) uninstall

# Uninstalls all simulation envs
uninstall:
	cd stopping_game/ && $(MAKE) uninstall
	cd stopping_mdp_attacker/ && $(MAKE) uninstall
	cd stopping_pomdp_defender/ && $(MAKE) uninstall

# Targets for cleaning the config each individual env
clean_config_stopping_game:
	cd stopping_game/ && $(MAKE) clean_config

clean_config_stopping_mdp_attacker:
	cd stopping_mdp_attacker/ && $(MAKE) clean_config

clean_config_stopping_pomdp_defender:
	cd stopping_pomdp_defender/ && $(MAKE) clean_config

# Cleans the materialized configuration of each emulation
clean_config:
	cd stopping_game/ && $(MAKE) clean_config
	cd stopping_mdp_attacker/ && $(MAKE) clean_config
	cd stopping_pomdp_defender/ && $(MAKE) clean_config
