# CSLE Metastore

CSLE stores metadata in a PostgreSQL Citus database.

<p align="center">
<img src="./../docs/img/postgres.png" width="250">
</p>

## Setup the metastore

Create database
```bash
make db
```
Create Citus cluster
```bash
make cluster
```
Create tables
```bash
make tables
```
You can also reset the database with the command:
```bash
make clean
```

Other useful psql commands: 
```bash
sudo -u postgres psql  # start psql session as admin user postgres
psql> \l # Lists databases
psql> \c csle # Connect to database csle
psql> \dt # List tables
psql> \du # List users
psql> \dn # List schemas
```

Commands for starting/restarting/stopping PostgreSql:
```
sudo service postgresql stop
sudo service postgresql start
sudo service postgresql restart
```

Logs:

```
tail /var/log/postgresql/postgresql-12-main.log 
```