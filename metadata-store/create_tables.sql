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
    emulation_id integer PRIMARY KEY NOT NULL,
    name TEXT UNIQUE NOT NULL
);

-- Create table that stores the running emulations --
CREATE TABLE IF NOT EXISTS running_emulations (
    emulation_id integer references emulations(emulation_id),
    dir TEXT UNIQUE NOT NULL
);

-- Create table that stores the vuln configurations --
CREATE TABLE IF NOT EXISTS vuln_configs (
    emulation_id integer references emulations(emulation_id),
    config jsonb
);

-- Create table that stores the topology configurations --
CREATE TABLE IF NOT EXISTS topology_configs (
    emulation_id integer references emulations(emulation_id),
    config jsonb
);

-- Create table that stores the flags configurations --
CREATE TABLE IF NOT EXISTS flags_configs (
    emulation_id integer references emulations(emulation_id),
    config jsonb
);

-- Create table that stores the container configurations --
CREATE TABLE IF NOT EXISTS containers_configs (
    emulation_id integer references emulations(emulation_id),
    config jsonb
);

-- Create table that stores the resource constraints configurations --
CREATE TABLE IF NOT EXISTS resources_configs (
    emulation_id integer references emulations(emulation_id),
    config jsonb
);

-- Create table that stores the traffic configurations --
CREATE TABLE IF NOT EXISTS traffic_configs (
    emulation_id integer references emulations(emulation_id),
    config jsonb
);

-- Create table that stores the containers configurations --
CREATE TABLE IF NOT EXISTS container_configs (
    emulation_id integer references emulations(emulation_id),
    config jsonb
);

-- Create table that stores the users configurations --
CREATE TABLE IF NOT EXISTS users_configs (
    emulation_id integer references emulations(emulation_id),
    config jsonb
);

