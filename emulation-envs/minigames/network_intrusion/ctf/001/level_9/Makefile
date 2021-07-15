all: run users topology vuln flags gen_containers_config traffic

run: gen_containers_config
	cd containers/router2/ && $(MAKE) run
	cd containers/ssh1/ && $(MAKE) run
	cd containers/shellshock1_1/ && $(MAKE) run
	cd containers/sql_injection1_1/ && $(MAKE) run
	cd containers/samba1_2/ && $(MAKE) run
	cd containers/cve_2010_0426_1_1/ && $(MAKE) run
	cd containers/cve_2015_1427_1_1/ && $(MAKE) run
	cd containers/honeypot1_1/ && $(MAKE) run
	cd containers/honeypot1_2/ && $(MAKE) run
	cd containers/honeypot1_3/ && $(MAKE) run
	cd containers/honeypot1_4/ && $(MAKE) run
	cd containers/honeypot1_5/ && $(MAKE) run
	cd containers/honeypot1_6/ && $(MAKE) run
	cd containers/cve_2015_3306_1_1/ && $(MAKE) run
	cd containers/honeypot2_1/ && $(MAKE) run
	cd containers/honeypot2_2/ && $(MAKE) run
	cd containers/honeypot2_3/ && $(MAKE) run
	cd containers/honeypot2_4/ && $(MAKE) run
	cd containers/honeypot2_5/ && $(MAKE) run
	cd containers/honeypot2_6/ && $(MAKE) run
	cd containers/honeypot2_7/ && $(MAKE) run
	cd containers/honeypot2_8/ && $(MAKE) run
	cd containers/honeypot2_9/ && $(MAKE) run
	cd containers/honeypot2_10/ && $(MAKE) run
	cd containers/honeypot2_11/ && $(MAKE) run
	cd containers/honeypot2_12/ && $(MAKE) run
	cd containers/honeypot2_13/ && $(MAKE) run
	cd containers/honeypot2_14/ && $(MAKE) run
	cd containers/cve_2015_5602_1_1/ && $(MAKE) run
	cd containers/cve_2016_10033_1_1/ && $(MAKE) run
	cd containers/ftp1/ && $(MAKE) run
	cd containers/samba1_1/ && $(MAKE) run
	cd containers/hacker_kali1/ && $(MAKE) run
	cd containers/client1_1/ && $(MAKE) run
	cd containers/client1_2/ && $(MAKE) run
	cd containers/client1_3/ && $(MAKE) run

stop:
	cd containers/router2/ && $(MAKE) stop
	cd containers/ssh1/ && $(MAKE) stop
	cd containers/shellshock1_1/ && $(MAKE) stop
	cd containers/sql_injection1_1/ && $(MAKE) stop
	cd containers/samba1_2/ && $(MAKE) stop
	cd containers/cve_2010_0426_1_1/ && $(MAKE) stop
	cd containers/cve_2015_1427_1_1/ && $(MAKE) stop
	cd containers/honeypot1_1/ && $(MAKE) stop
	cd containers/honeypot1_2/ && $(MAKE) stop
	cd containers/honeypot1_3/ && $(MAKE) stop
	cd containers/honeypot1_4/ && $(MAKE) stop
	cd containers/honeypot1_5/ && $(MAKE) stop
	cd containers/honeypot1_6/ && $(MAKE) stop
	cd containers/cve_2015_3306_1_1/ && $(MAKE) stop
	cd containers/honeypot2_1/ && $(MAKE) stop
	cd containers/honeypot2_2/ && $(MAKE) stop
	cd containers/honeypot2_3/ && $(MAKE) stop
	cd containers/honeypot2_4/ && $(MAKE) stop
	cd containers/honeypot2_5/ && $(MAKE) stop
	cd containers/honeypot2_6/ && $(MAKE) stop
	cd containers/honeypot2_7/ && $(MAKE) stop
	cd containers/honeypot2_8/ && $(MAKE) stop
	cd containers/honeypot2_9/ && $(MAKE) stop
	cd containers/honeypot2_10/ && $(MAKE) stop
	cd containers/honeypot2_11/ && $(MAKE) stop
	cd containers/honeypot2_12/ && $(MAKE) stop
	cd containers/honeypot2_13/ && $(MAKE) stop
	cd containers/honeypot2_14/ && $(MAKE) stop
	cd containers/cve_2015_5602_1_1/ && $(MAKE) stop
	cd containers/cve_2016_10033_1_1/ && $(MAKE) stop
	cd containers/ftp1/ && $(MAKE) stop
	cd containers/samba1_1/ && $(MAKE) stop
	cd containers/hacker_kali1/ && $(MAKE) stop
	cd containers/client1_1/ && $(MAKE) stop
	cd containers/client1_2/ && $(MAKE) stop
	cd containers/client1_3/ && $(MAKE) stop

start:
	cd containers/router2/ && $(MAKE) start
	cd containers/ssh1/ && $(MAKE) start
	cd containers/shellshock1_1/ && $(MAKE) start
	cd containers/sql_injection1_1/ && $(MAKE) start
	cd containers/samba1_2/ && $(MAKE) start
	cd containers/cve_2010_0426_1_1/ && $(MAKE) start
	cd containers/cve_2015_1427_1_1/ && $(MAKE) start
	cd containers/honeypot1_1/ && $(MAKE) start
	cd containers/honeypot1_2/ && $(MAKE) start
	cd containers/honeypot1_3/ && $(MAKE) start
	cd containers/honeypot1_4/ && $(MAKE) start
	cd containers/honeypot1_5/ && $(MAKE) start
	cd containers/honeypot1_6/ && $(MAKE) start
	cd containers/cve_2015_3306_1_1/ && $(MAKE) start
	cd containers/honeypot2_1/ && $(MAKE) start
	cd containers/honeypot2_2/ && $(MAKE) start
	cd containers/honeypot2_3/ && $(MAKE) start
	cd containers/honeypot2_4/ && $(MAKE) start
	cd containers/honeypot2_5/ && $(MAKE) start
	cd containers/honeypot2_6/ && $(MAKE) start
	cd containers/honeypot2_7/ && $(MAKE) start
	cd containers/honeypot2_8/ && $(MAKE) start
	cd containers/honeypot2_9/ && $(MAKE) start
	cd containers/honeypot2_10/ && $(MAKE) start
	cd containers/honeypot2_11/ && $(MAKE) start
	cd containers/honeypot2_12/ && $(MAKE) start
	cd containers/honeypot2_13/ && $(MAKE) start
	cd containers/honeypot2_14/ && $(MAKE) start
	cd containers/cve_2015_5602_1_1/ && $(MAKE) start
	cd containers/cve_2016_10033_1_1/ && $(MAKE) start
	cd containers/ftp1/ && $(MAKE) start
	cd containers/samba1_1/ && $(MAKE) start
	cd containers/hacker_kali1/ && $(MAKE) start
	cd containers/client1_1/ && $(MAKE) start
	cd containers/client1_2/ && $(MAKE) start
	cd containers/client1_3/ && $(MAKE) start
	python create_topology.py

clean: stop
	cd containers/router2/ && $(MAKE) clean
	cd containers/ssh1/ && $(MAKE) clean
	cd containers/shellshock1_1/ && $(MAKE) clean
	cd containers/sql_injection1_1/ && $(MAKE) clean
	cd containers/samba1_2 && $(MAKE) clean
	cd containers/cve_2010_0426_1_1/ && $(MAKE) clean
	cd containers/cve_2015_1427_1_1/ && $(MAKE) clean
	cd containers/honeypot1_1/ && $(MAKE) clean
	cd containers/honeypot1_2/ && $(MAKE) clean
	cd containers/honeypot1_3/ && $(MAKE) clean
	cd containers/honeypot1_4/ && $(MAKE) clean
	cd containers/honeypot1_5/ && $(MAKE) clean
	cd containers/honeypot1_6/ && $(MAKE) clean
	cd containers/cve_2015_3306_1_1/ && $(MAKE) clean
	cd containers/honeypot2_1/ && $(MAKE) clean
	cd containers/honeypot2_2/ && $(MAKE) clean
	cd containers/honeypot2_3/ && $(MAKE) clean
	cd containers/honeypot2_4/ && $(MAKE) clean
	cd containers/honeypot2_5/ && $(MAKE) clean
	cd containers/honeypot2_6/ && $(MAKE) clean
	cd containers/honeypot2_7/ && $(MAKE) clean
	cd containers/honeypot2_8/ && $(MAKE) clean
	cd containers/honeypot2_9/ && $(MAKE) clean
	cd containers/honeypot2_10/ && $(MAKE) clean
	cd containers/honeypot2_11/ && $(MAKE) clean
	cd containers/honeypot2_12/ && $(MAKE) clean
	cd containers/honeypot2_13/ && $(MAKE) clean
	cd containers/honeypot2_14/ && $(MAKE) clean
	cd containers/cve_2015_5602_1_1/ && $(MAKE) clean
	cd containers/cve_2016_10033_1_1/ && $(MAKE) clean
	cd containers/ftp1/ && $(MAKE) clean
	cd containers/samba1_1/ && $(MAKE) clean
	cd containers/hacker_kali1/ && $(MAKE) clean
	cd containers/client1_1/ && $(MAKE) clean
	cd containers/client1_2/ && $(MAKE) clean
	cd containers/client1_3/ && $(MAKE) clean

apply_config: users vuln flags topology gen_containers_config

topology: ./create_topology.py
	python create_topology.py

users: ./create_users.py
	python create_users.py

flags: ./create_flags.py
	python create_flags.py

vuln: ./create_vuln.py
	python create_vuln.py

gen_containers_config: ./gen_containers_config.py
	python gen_containers_config.py


clean_fs_cache:
	python clean_fs_cache.py

traffic: ./create_traffic_generators.py
	python create_traffic_generators.py

stop_traffic: ./stop_traffic_generators.py
	python stop_traffic_generators.py

clean_config:
	rm -rf ./users.json
	rm -rf ./vulnerabilities.json
	rm -rf ./flags.json
	rm -rf ./containers.json
	rm -rf ./topology.json
	rm -rf ./containers.json
	rm -rf ./traffic.json
