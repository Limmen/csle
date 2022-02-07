PROJECT=csle
VERSION=0.0.1

all: build

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
