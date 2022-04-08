# Targets for installing each individual env
install_stopping_game:
	cd 001/stopping_game/ && $(MAKE) install

install_stopping_mdp_attacker:
	cd 001/stopping_mdp_attacker/ && $(MAKE) install

install_stopping_pomdp_defender:
	cd 001/stopping_pomdp_defender/ && $(MAKE) install

# Installs all emulations
install:
	cd 001/stopping_game/ && $(MAKE) install
	cd 001/stopping_mdp_attacker/ && $(MAKE) install
	cd 001/stopping_pomdp_defender/ && $(MAKE) install

# Targets for uninstalling each individual env
uninstall_stopping_game:
	cd 001/stopping_game/ && $(MAKE) uninstall

uninstall_stopping_mdp_attacker:
	cd 001/stopping_mdp_attacker/ && $(MAKE) uninstall

uninstall_stopping_pomdp_defender:
	cd 001/stopping_pomdp_defender/ && $(MAKE) uninstall

# Uninstalls all simulation envs
uninstall:
	cd 001/stopping_game/ && $(MAKE) uninstall
	cd 001/stopping_mdp_attacker/ && $(MAKE) uninstall
	cd 001/stopping_pomdp_defender/ && $(MAKE) uninstall

# Targets for cleaning the config each individual env
clean_config_stopping_game:
	cd 001/stopping_game/ && $(MAKE) clean_config

clean_config_stopping_mdp_attacker:
	cd 001/stopping_mdp_attacker/ && $(MAKE) clean_config

clean_config_stopping_pomdp_defender:
	cd 001/stopping_pomdp_defender/ && $(MAKE) clean_config

# Cleans the materialized configuration of each emulation
clean_config:
	cd 001/stopping_game/ && $(MAKE) clean_config
	cd 001/stopping_mdp_attacker/ && $(MAKE) clean_config
	cd 001/stopping_pomdp_defender/ && $(MAKE) clean_config
