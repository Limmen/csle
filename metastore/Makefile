PROJECT=csle
VERSION=0.0.1

all: build

# Setup Citus (should be done before build)
citus:
	sudo psql -U postgres -a -f make_db.sql

# Setup cluster (should be done before build and after citus)
cluster:
	sudo psql -U postgres -a -f create_cluster.sql

# Create db, users, and tables
build:
	sudo psql -U postgres -a -f create_tables.sql

# Start a postgresql shell
psql:
	sudo -u postgres psql

# Drop db
clean:
	-sudo psql -U postgres -a --command='drop database csle'

# Restarts postgresql
restart:
	sudo service postgresql restart
