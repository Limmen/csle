# Metastore

CSLE stores metadata in a PostgreSQL database. Follow the steps below to install PostgreSQL and setup the database.

## Setup PostgreSQL

Install postgresql:
```bash
sudo apt-get install postgresql # install postgresql
sudo apt-get install libpq-dev # install dependencies
```

Set a password for the postgres user:
```bash
sudo -u postgres psql  # start psql session as admin user posgres
psql> \password postgres # set postgres password
```

Setup password authentication for user postgres:
1. Open file `/etc/postgresql/10/main/pg_hba.conf`
2. Change `peer` to `md5` on line: `local all postgres peer`
3. Save and close the file
4. Restart postgres with the command `sudo service postgresql restart`

Create database and tables:
```bash
sudo psql -U postgres -a -f create_tables.sql
```
Or by using the command:
```bash
make build
```
You can also reset the database with the command:
```bash
make clean
```

Other useful psql commands: 
```bash
sudo -u postgres psql  # start psql session as admin user posgres
psql> \l # Lists databases
psql> \c csle # Connect to database csle
psql> \dt # List tables
psql> \du # List users
psql> \dn # List schemas
```

Commands for starting/restarting/stopping postrgresql:
```
sudo service postgresql stop
sudo service postgresql start
sudo service postgresql restart
```
Logs:

```
tail /var/log/postgresql/postgresql-12-main.log 
```