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

-- Create table that stores the emulation traces --
CREATE TABLE IF NOT EXISTS emulation_traces (
    id serial PRIMARY KEY,
    emulation_name TEXT references emulations(name) ON DELETE CASCADE,
    trace json NOT NULL
);
GRANT ALL ON emulation_traces TO csle;
GRANT USAGE, SELECT ON SEQUENCE emulation_traces_id_seq TO csle;

-- Create table that stores the emulation statistics --
CREATE TABLE IF NOT EXISTS emulation_statistics (
    id serial PRIMARY KEY,
    emulation_name TEXT references emulations(name) ON DELETE CASCADE,
    statistics json NOT NULL
);
GRANT ALL ON emulation_statistics TO csle;
GRANT USAGE, SELECT ON SEQUENCE emulation_statistics_id_seq TO csle;

-- Create table that stores the simulation traces --
CREATE TABLE IF NOT EXISTS simulation_traces (
    id serial PRIMARY KEY,
    gym_env TEXT NOT NULL,
    trace json NOT NULL
);
GRANT ALL ON simulation_traces TO csle;
GRANT USAGE, SELECT ON SEQUENCE simulation_traces_id_seq TO csle;

-- Create table that stores the emulation-simulation traces --
CREATE TABLE IF NOT EXISTS emulation_simulation_traces (
    id serial PRIMARY KEY,
    emulation_trace int NOT NULL references emulation_traces(id) ON DELETE CASCADE,
    simulation_trace int NOT NULL references simulation_traces(id) ON DELETE CASCADE
);
GRANT ALL ON emulation_simulation_traces TO csle;
GRANT USAGE, SELECT ON SEQUENCE emulation_simulation_traces_id_seq TO csle;

-- Create table that stores the emulation images --
CREATE TABLE IF NOT EXISTS emulation_images (
    id serial PRIMARY KEY,
    emulation_name TEXT references emulations(name) ON DELETE CASCADE,
    image bytea NOT NULL
    );
GRANT ALL ON emulation_images TO csle;
GRANT USAGE, SELECT ON SEQUENCE emulation_images_id_seq TO csle;

-- Create table that stores the simulations --
CREATE TABLE IF NOT EXISTS simulations (
    id serial PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    emulation_statistic_id int NOT NULL references emulation_statistics(id) ON DELETE CASCADE,
    config json NOT NULL
);
GRANT ALL ON simulations TO csle;
GRANT USAGE, SELECT ON SEQUENCE simulations_id_seq TO csle;

-- Create table that stores the experiment executions --
CREATE TABLE IF NOT EXISTS experiment_executions (
    id serial PRIMARY KEY,
    execution json NOT NULL
);
GRANT ALL ON experiment_executions TO csle;
GRANT USAGE, SELECT ON SEQUENCE experiment_executions_id_seq TO csle;