all: run users topology flags vuln

.PHONY: run

generate_envs:
	python generate_config.py

topology:
	python make_cmd.py --c topology

users:
	python make_cmd.py --c users

flags:
	python make_cmd.py --c flags

vuln:
	python make_cmd.py --c vuln

clean_config:
	python make_cmd.py --c clean_config

gen_config:
	python make_cmd.py --c gen_config


apply_config: users vuln topology flags

run:
	python make_cmd.py --c run

stop:
	python make_cmd.py --c stop

start:
	python make_cmd.py --c start

clean:
	python make_cmd.py --c clean

clean_envs:
	python make_cmd.py --c clean_envs


