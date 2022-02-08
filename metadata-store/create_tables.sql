--  Create csle db if not exists --
SELECT 'CREATE DATABASE csle'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'csle')\gexec

-- Connect to the csle db --
\connect csle

-- Create csle user --
REASSIGN OWNED BY csle TO postgres;
DROP OWNED BY csle;
DROP USER IF EXISTS csle;
CREATE USER csle WITH ENCRYPTED PASSWORD 'csle';

-- Grant priviliges to csle user for the csle db --
GRANT ALL PRIVILEGES ON DATABASE csle TO csle;

-- Create table that stores the emulations --
CREATE TABLE IF NOT EXISTS emulations (
    id serial PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    config json NOT NULL
);
GRANT ALL ON emulations TO csle;
GRANT USAGE, SELECT ON SEQUENCE emulations_id_seq TO csle;

-- Create table that stores the running emulations --
CREATE TABLE IF NOT EXISTS running_emulations (
    emulation_id serial references emulations(id),
    dir TEXT UNIQUE NOT NULL
);

GRANT ALL ON running_emulations TO csle;

