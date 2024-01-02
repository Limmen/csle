-- Connect to the csle db --
\connect csle

-- Create table that stores the emulations --
CREATE TABLE IF NOT EXISTS emulations (
    id serial PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    config json NOT NULL
);
GRANT ALL ON emulations TO csle;
GRANT USAGE, SELECT ON SEQUENCE emulations_id_seq TO csle;
SELECT create_reference_table('emulations');

-- Create table that stores the emulation traces --
CREATE TABLE IF NOT EXISTS emulation_traces (
    id serial PRIMARY KEY,
    emulation_name TEXT references emulations(name) ON DELETE CASCADE,
    trace bytea NOT NULL
);
GRANT ALL ON emulation_traces TO csle;
GRANT USAGE, SELECT ON SEQUENCE emulation_traces_id_seq TO csle;
SELECT create_reference_table('emulation_traces');

-- Create table that stores the emulation statistics --
CREATE TABLE IF NOT EXISTS emulation_statistics (
    id serial PRIMARY KEY,
    emulation_name TEXT references emulations(name) ON DELETE CASCADE,
    statistics bytea NOT NULL
);
GRANT ALL ON emulation_statistics TO csle;
GRANT USAGE, SELECT ON SEQUENCE emulation_statistics_id_seq TO csle;
SELECT create_reference_table('emulation_statistics');

-- Create table that stores the simulation traces --
CREATE TABLE IF NOT EXISTS simulation_traces (
    id serial PRIMARY KEY,
    gym_env TEXT NOT NULL,
    trace json NOT NULL
);
GRANT ALL ON simulation_traces TO csle;
GRANT USAGE, SELECT ON SEQUENCE simulation_traces_id_seq TO csle;
SELECT create_reference_table('simulation_traces');

-- Create table that stores the emulation-simulation traces --
CREATE TABLE IF NOT EXISTS emulation_simulation_traces (
    id serial PRIMARY KEY,
    emulation_trace int NOT NULL references emulation_traces(id) ON DELETE CASCADE,
    simulation_trace int NOT NULL references simulation_traces(id) ON DELETE CASCADE
);
GRANT ALL ON emulation_simulation_traces TO csle;
GRANT USAGE, SELECT ON SEQUENCE emulation_simulation_traces_id_seq TO csle;
SELECT create_reference_table('emulation_simulation_traces');

-- Create table that stores the emulation images --
CREATE TABLE IF NOT EXISTS emulation_images (
    id serial PRIMARY KEY,
    emulation_name TEXT references emulations(name) ON DELETE CASCADE,
    image bytea NOT NULL
    );
GRANT ALL ON emulation_images TO csle;
GRANT USAGE, SELECT ON SEQUENCE emulation_images_id_seq TO csle;
SELECT create_reference_table('emulation_images');

-- Create table that stores the simulations --
CREATE TABLE IF NOT EXISTS simulations (
    id serial PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    config json NOT NULL
);
GRANT ALL ON simulations TO csle;
GRANT USAGE, SELECT ON SEQUENCE simulations_id_seq TO csle;
SELECT create_reference_table('simulations');

-- Create table that stores the experiment executions --
CREATE TABLE IF NOT EXISTS experiment_executions (
    id serial PRIMARY KEY,
    execution json NOT NULL,
    simulation_name TEXT references simulations(name),
    emulation_name TEXT references emulations(name)
);
GRANT ALL ON experiment_executions TO csle;
GRANT USAGE, SELECT ON SEQUENCE experiment_executions_id_seq TO csle;
SELECT create_reference_table('experiment_executions');

-- Create table that stores the simulation images --
CREATE TABLE IF NOT EXISTS simulation_images (
    id serial PRIMARY KEY,
    simulation_name TEXT references simulations(name) ON DELETE CASCADE,
    image bytea NOT NULL
);
GRANT ALL ON simulation_images TO csle;
GRANT USAGE, SELECT ON SEQUENCE simulation_images_id_seq TO csle;
SELECT create_reference_table('simulation_images');

-- Create table that stores the multi_threshold_stopping_policies --
CREATE TABLE IF NOT EXISTS multi_threshold_stopping_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON multi_threshold_stopping_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE multi_threshold_stopping_policies_id_seq TO csle;
SELECT create_reference_table('multi_threshold_stopping_policies');

-- Create table that stores training jobs --
CREATE TABLE IF NOT EXISTS training_jobs (
    id serial PRIMARY KEY,
    config json NOT NULL,
    simulation_name TEXT references simulations(name) ON DELETE CASCADE,
    emulation_name TEXT references emulations(name) ON DELETE CASCADE,
    pid int NOT NULL
);
GRANT ALL ON training_jobs TO csle;
GRANT USAGE, SELECT ON SEQUENCE training_jobs_id_seq TO csle;
SELECT create_reference_table('training_jobs');

-- Create table that stores system_identification_jobs --
CREATE TABLE IF NOT EXISTS system_identification_jobs (
    id serial PRIMARY KEY,
    config json NOT NULL,
    emulation_name TEXT references emulations(name),
    pid int NOT NULL
);
GRANT ALL ON system_identification_jobs TO csle;
GRANT USAGE, SELECT ON SEQUENCE system_identification_jobs_id_seq TO csle;
SELECT create_reference_table('system_identification_jobs');

-- Create table that stores the ppo_policies --
CREATE TABLE IF NOT EXISTS ppo_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON ppo_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE ppo_policies_id_seq TO csle;
SELECT create_reference_table('ppo_policies');

-- Create table that stores the system_models --
CREATE TABLE IF NOT EXISTS system_models (
    id serial PRIMARY KEY,
    emulation_name TEXT references emulations(name) ON DELETE CASCADE,
    system_model json NOT NULL
    );
GRANT ALL ON system_models TO csle;
GRANT USAGE, SELECT ON SEQUENCE system_models_id_seq TO csle;
SELECT create_reference_table('system_models');

-- Create table that stores system_identification_jobs --
CREATE TABLE IF NOT EXISTS data_collection_jobs (
    id serial PRIMARY KEY,
    config json NOT NULL,
    emulation_name TEXT references emulations(name),
    pid int NOT NULL
    );
GRANT ALL ON data_collection_jobs TO csle;
GRANT USAGE, SELECT ON SEQUENCE data_collection_jobs_id_seq TO csle;
SELECT create_reference_table('data_collection_jobs');

-- Create table that stores the gaussian mixture system models --
CREATE TABLE IF NOT EXISTS gaussian_mixture_system_models (
    id serial PRIMARY KEY,
    model json NOT NULL,
    emulation_name TEXT references emulations(name),
    emulation_statistic_id int references emulation_statistics(id)
    );
GRANT ALL ON gaussian_mixture_system_models TO csle;
GRANT USAGE, SELECT ON SEQUENCE gaussian_mixture_system_models_id_seq TO csle;
SELECT create_reference_table('gaussian_mixture_system_models');

-- Create table that stores the tabular_policies --
CREATE TABLE IF NOT EXISTS tabular_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON tabular_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE tabular_policies_id_seq TO csle;
SELECT create_reference_table('tabular_policies');

-- Create table that stores the alpha_vec_policies --
CREATE TABLE IF NOT EXISTS alpha_vec_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON alpha_vec_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE alpha_vec_policies_id_seq TO csle;
SELECT create_reference_table('alpha_vec_policies');

-- Create table that stores the dqn_policies --
CREATE TABLE IF NOT EXISTS dqn_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON dqn_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE dqn_policies_id_seq TO csle;
SELECT create_reference_table('dqn_policies');

-- Create table that stores the fnn_w_softmax_policies --
CREATE TABLE IF NOT EXISTS fnn_w_softmax_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON fnn_w_softmax_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE fnn_w_softmax_policies_id_seq TO csle;
SELECT create_reference_table('fnn_w_softmax_policies');

-- Create table that stores the vector policies --
CREATE TABLE IF NOT EXISTS vector_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
    );
GRANT ALL ON vector_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE vector_policies_id_seq TO csle;
SELECT create_reference_table('vector_policies');

-- Create table that stores emulation executions --
CREATE TABLE IF NOT EXISTS emulation_executions (
    ip_first_octet int NOT NULL,
    emulation_name TEXT references emulations(name) ON DELETE CASCADE,
    info json NOT NULL,
    PRIMARY KEY (ip_first_octet, emulation_name)
);
GRANT ALL ON emulation_executions TO csle;
SELECT create_reference_table('emulation_executions');

-- Create table that stores the empirical system models --
CREATE TABLE IF NOT EXISTS empirical_system_models (
    id serial PRIMARY KEY,
    model json NOT NULL,
    emulation_name TEXT references emulations(name),
    emulation_statistic_id int references emulation_statistics(id)
);
GRANT ALL ON empirical_system_models TO csle;
GRANT USAGE, SELECT ON SEQUENCE empirical_system_models_id_seq TO csle;
SELECT create_reference_table('empirical_system_models');

-- Create table that stores the gp system models --
CREATE TABLE IF NOT EXISTS gp_system_models (
    id serial PRIMARY KEY,
    model json NOT NULL,
    emulation_name TEXT references emulations(name),
    emulation_statistic_id int references emulation_statistics(id)
);
GRANT ALL ON gp_system_models TO csle;
GRANT USAGE, SELECT ON SEQUENCE gp_system_models_id_seq TO csle;
SELECT create_reference_table('gp_system_models');

-- Create table that stores the management user accounts --
CREATE TABLE IF NOT EXISTS management_users (
    id serial PRIMARY KEY,
    username VARCHAR(128) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    email varchar(254) NOT NULL,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    organization varchar(255) NOT NULL,
    admin BOOLEAN NOT NULL,
    salt VARCHAR(128) NOT NULL
);
GRANT ALL ON management_users TO csle;
GRANT USAGE, SELECT ON SEQUENCE management_users_id_seq TO csle;
SELECT create_reference_table('management_users');

-- Create table that stores the session tokens --
CREATE TABLE IF NOT EXISTS session_tokens (
    token VARCHAR(128) UNIQUE NOT NULL PRIMARY KEY,
    timestamp DOUBLE PRECISION NOT NULL,
    username VARCHAR(128) UNIQUE references management_users(username)
);
GRANT ALL ON session_tokens TO csle;
SELECT create_reference_table('session_tokens');

-- Create table that stores the traces datasets metadata --
CREATE TABLE IF NOT EXISTS traces_datasets (
    id serial PRIMARY KEY,
    name VARCHAR(128) UNIQUE NOT NULL,
    description TEXT,
    data_schema json,
    download_count int NOT NULL,
    file_path VARCHAR(1024),
    url VARCHAR(1024),
    date_added TIMESTAMP NOT NULL,
    num_traces int NOT NULL,
    num_attributes_per_time_step int NOT NULL,
    size_in_gb DOUBLE PRECISION NOT NULL,
    compressed_size_in_gb DOUBLE PRECISION NOT NULL,
    citation TEXT,
    num_files int NOT NULL,
    file_format VARCHAR(128) NOT NULL,
    added_by VARCHAR(1024) NOT NULL,
    columns TEXT
);
GRANT ALL ON traces_datasets TO csle;
GRANT USAGE, SELECT ON SEQUENCE traces_datasets_id_seq TO csle;
SELECT create_reference_table('traces_datasets');

-- Create table that stores the statistics datasets metadata --
CREATE TABLE IF NOT EXISTS statistics_datasets (
    id serial PRIMARY KEY,
    name VARCHAR(128) UNIQUE NOT NULL,
    description TEXT,
    download_count int NOT NULL,
    file_path VARCHAR(1024),
    url VARCHAR(1024),
    date_added TIMESTAMP NOT NULL,
    num_measurements int NOT NULL,
    num_metrics int NOT NULL,
    size_in_gb DOUBLE PRECISION NOT NULL,
    compressed_size_in_gb DOUBLE PRECISION NOT NULL,
    citation TEXT,
    num_files int NOT NULL,
    file_format VARCHAR(128) NOT NULL,
    added_by VARCHAR(1024) NOT NULL,
    conditions TEXT NOT NULL,
    metrics TEXT NOT NULL,
    num_conditions int NOT NULL
);
GRANT ALL ON statistics_datasets TO csle;
GRANT USAGE, SELECT ON SEQUENCE statistics_datasets_id_seq TO csle;
SELECT create_reference_table('statistics_datasets');

-- Create table that stores the config --
CREATE TABLE IF NOT EXISTS config (
    id int PRIMARY KEY,
    config json NOT NULL
);
GRANT ALL ON config TO csle;
SELECT create_reference_table('config');

-- Create table that stores the linear_threshold_stopping_policies --
CREATE TABLE IF NOT EXISTS linear_threshold_stopping_policies (
    id serial PRIMARY KEY,
    policy json NOT NULL,
    simulation_name TEXT references simulations(name)
);
GRANT ALL ON linear_threshold_stopping_policies TO csle;
GRANT USAGE, SELECT ON SEQUENCE linear_threshold_stopping_policies_id_seq TO csle;
SELECT create_reference_table('linear_threshold_stopping_policies');

-- Create table that stores the mcmc system models --
CREATE TABLE IF NOT EXISTS mcmc_system_models (
    id serial PRIMARY KEY,
    model json NOT NULL,
    emulation_name TEXT references emulations(name),
    emulation_statistic_id int references emulation_statistics(id)
);
GRANT ALL ON mcmc_system_models TO csle;
GRANT USAGE, SELECT ON SEQUENCE mcmc_system_models_id_seq TO csle;
SELECT create_reference_table('mcmc_system_models');