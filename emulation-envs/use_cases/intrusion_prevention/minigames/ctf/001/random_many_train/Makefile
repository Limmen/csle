all: run users topology vuln flags traffic

.PHONY: run

# Generate the environment configurations
generate_envs:
	python generate_config.py

# Applies the 'make topology' command to all environments
topology:
	python make_cmd.py --c topology

# Applies the 'make users' command to all environments
users:
	python make_cmd.py --c users

# Applies the 'make flags' command to all environments
flags:
	python make_cmd.py --c flags

# Applies the 'make vuln' command to all environments
vuln:
	python make_cmd.py --c vuln

# Applies the 'make traffic' command to all environments
traffic:
	python make_cmd.py --c traffic

# Applies the 'make clean_config' command to all environments
clean_config:
	python make_cmd.py --c clean_config

# Applies the 'make gen_config' command to all environments
gen_config:
	python make_cmd.py --c gen_config

# Applies the config to all environments
apply_config: users vuln topology flags

# Applies the 'make run' command to all environments
run:
	python make_cmd.py --c run

# Applies the 'make stop' command to all environments
stop:
	python make_cmd.py --c stop

# Starts the container (assumes that it has previously been created and stopped)
start:
	python make_cmd.py --c start

# Applies the 'make clean' command to all environments
clean:
	python make_cmd.py --c clean

# Applies the 'make clean_envs' command to all environments
clean_envs:
	python make_cmd.py --c clean_envs

# Applies the 'make clean_fs_cache' command to all environments
clean_fs_cache:
	python make_cmd.py --c clean_fs_cache