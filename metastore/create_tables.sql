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
    config json NOT NULL
);
GRANT ALL ON simulations TO csle;
GRANT USAGE, SELECT ON SEQUENCE simulations_id_seq TO csle;

-- Create table that stores the experiment executions --
CREATE TABLE IF NOT EXISTS experiment_executions (
    id serial PRIMARY KEY,
    execution json NOT NULL,
    simulation_name TEXT references simulations(name),
    emulation_name TEXT references emulations(name)
);
GRANT ALL ON experiment_executions TO csle;
GRANT USAGE, SELECT ON SEQUENCE experiment_executions_id_seq TO csle;

-- Create table that stores the simulation images --
CREATE TABLE IF NOT EXISTS simulation_images (
    id serial PRIMARY KEY,
    simulation_name TEXT references simulations(name) ON DELETE CASCADE,
    image bytea NOT NULL
);
GRANT ALL ON simulation_images TO csle;
GRANT USAGE, SELECT ON SEQUENCE simulation_images_id_seq TO csle;

-- Create table that stores the multi_threshold_stopping_policies --
CREATE TABLE IF NOT EXISTS multi_threshold_stopping_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON multi_threshold_stopping_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE multi_threshold_stopping_policies_id_seq TO csle;

-- Create table that stores training jobs --
CREATE TABLE IF NOT EXISTS training_jobs (
    id serial PRIMARY KEY,
    config json NOT NULL,
    simulation_name TEXT references simulations(name) ON DELETE CASCADE,
    emulation_name TEXT references emulations(name) ON DELETE CASCADE
);
GRANT ALL ON training_jobs TO csle;
GRANT USAGE, SELECT ON SEQUENCE training_jobs_id_seq TO csle;

-- Create table that stores system_identification_jobs --
CREATE TABLE IF NOT EXISTS system_identification_jobs (
    id serial PRIMARY KEY,
    config json NOT NULL,
    emulation_name TEXT references emulations(name)
);
GRANT ALL ON system_identification_jobs TO csle;
GRANT USAGE, SELECT ON SEQUENCE system_identification_jobs_id_seq TO csle;

-- Create table that stores the ppo_policies --
CREATE TABLE IF NOT EXISTS ppo_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON ppo_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE ppo_policies_id_seq TO csle;

-- Create table that stores the system_models --
CREATE TABLE IF NOT EXISTS system_models (
    id serial PRIMARY KEY,
    emulation_name TEXT references emulations(name) ON DELETE CASCADE,
    system_model json NOT NULL
    );
GRANT ALL ON system_models TO csle;
GRANT USAGE, SELECT ON SEQUENCE system_models_id_seq TO csle;

-- Create table that stores system_identification_jobs --
CREATE TABLE IF NOT EXISTS data_collection_jobs (
    id serial PRIMARY KEY,
    config json NOT NULL,
    emulation_name TEXT references emulations(name)
    );
GRANT ALL ON data_collection_jobs TO csle;
GRANT USAGE, SELECT ON SEQUENCE data_collection_jobs_id_seq TO csle;

-- Create table that stores the gaussian mixture system models --
CREATE TABLE IF NOT EXISTS gaussian_mixture_system_models (
    id serial PRIMARY KEY,
    model json NOT NULL,
    emulation_name TEXT references emulations(name),
    emulation_statistic_id int references emulation_statistics(id)
    );
GRANT ALL ON gaussian_mixture_system_models TO csle;
GRANT USAGE, SELECT ON SEQUENCE gaussian_mixture_system_models_id_seq TO csle;

-- Create table that stores the tabular_policies --
CREATE TABLE IF NOT EXISTS tabular_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON tabular_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE tabular_policies_id_seq TO csle;

-- Create table that stores the alpha_vec_policies --
CREATE TABLE IF NOT EXISTS alpha_vec_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON alpha_vec_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE alpha_vec_policies_id_seq TO csle;

-- Create table that stores the dqn_policies --
CREATE TABLE IF NOT EXISTS dqn_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON dqn_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE dqn_policies_id_seq TO csle;