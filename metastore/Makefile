all: db cluster tables

# Drops the csle citus db
drop:
	sudo psql -U postgres -a -f drop_tables.sql
	sudo psql -U postgres -a -f drop_db.sql

# Setup db and citus (should be done before build)
db:
	sudo psql -U postgres -a -f create_db_manual.sql

# Setup cluster (should be done before build and after citus)
cluster:
	sudo psql -U postgres -a -f create_cluster.sql

# Create db, users, and tables
tables:
	sudo psql -U postgres -a -f create_tables.sql

# Start a postgresql shell
psql:
	sudo -u postgres psql

# Drop db
clean:
	sudo psql -U postgres -a -f drop_db.sql

# Restarts postgresql
restart:
	sudo service postgresql restart
