
.PHONY: install run_all prometheus c_advisor grafana node_exporter list_stopped list_running list_images stop_running rm_stopped rm_images start_stopped

install:
	./install.sh

run_all:
	./run_all.sh

prometheus:
	./run_prometheus.sh

c_advisor:
	./run_c_advisor.sh

grafana:
	./run_grafana.sh

node_exporter:
	./run_node_exporter.sh

management_system:
	./run_mgmt_webapp.sh

list_stopped:
	python manage_containers.py --c list_stopped

list_running:
	python manage_containers.py --c list_running

list_images:
	python manage_containers.py --c list_images

list_networks:
	python manage_containers.py --c list_networks



stop_running:
	python manage_containers.py --c stop_running

rm_stopped:
	python manage_containers.py --c rm_stopped

rm_images:
	python manage_containers.py --c rm_images

rm_networks:
	python manage_containers.py --c rm_networks

start_stopped:
	python manage_containers.py --c start_stopped

clean_docker:
	docker system prune
