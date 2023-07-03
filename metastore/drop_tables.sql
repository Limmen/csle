DROP TABLE IF EXISTS emulations CASCADE;
DROP SEQUENCE IF EXISTS emulations_id_seq CASCADE;

DROP TABLE IF EXISTS emulation_traces CASCADE;
DROP SEQUENCE IF EXISTS emulation_traces_id_seq CASCADE;

DROP TABLE IF EXISTS emulation_statistics CASCADE;
DROP SEQUENCE IF EXISTS emulation_statistics_id_seq CASCADE;

DROP TABLE IF EXISTS simulation_traces CASCADE;
DROP SEQUENCE IF EXISTS simulation_traces_id_seq CASCADE;

DROP TABLE IF EXISTS emulation_simulation_traces CASCADE;
DROP SEQUENCE IF EXISTS emulation_simulation_traces_id_seq CASCADE;

DROP TABLE IF EXISTS emulation_images CASCADE;
DROP SEQUENCE IF EXISTS emulation_images_id_seq CASCADE;

DROP TABLE IF EXISTS simulations CASCADE;
DROP SEQUENCE IF EXISTS simulations_id_seq CASCADE;

DROP TABLE IF EXISTS experiment_executions CASCADE;
DROP SEQUENCE IF EXISTS experiment_executions_id_seq CASCADE;

DROP TABLE IF EXISTS simulation_images CASCADE;
DROP SEQUENCE IF EXISTS simulation_images_id_seq CASCADE;

DROP TABLE IF EXISTS multi_threshold_stopping_policies CASCADE;
DROP SEQUENCE IF EXISTS multi_threshold_stopping_policies_id_seq CASCADE;

DROP TABLE IF EXISTS training_jobs CASCADE;
DROP SEQUENCE IF EXISTS training_jobs_id_seq CASCADE;

DROP TABLE IF EXISTS system_identification_jobs CASCADE;
DROP SEQUENCE IF EXISTS system_identification_jobs_id_seq CASCADE;

DROP TABLE IF EXISTS ppo_policies CASCADE;
DROP SEQUENCE IF EXISTS ppo_policies_id_seq CASCADE;

DROP TABLE IF EXISTS system_models CASCADE;
DROP SEQUENCE IF EXISTS system_models_id_seq CASCADE;

DROP TABLE IF EXISTS data_collection_jobs CASCADE;
DROP SEQUENCE IF EXISTS data_collection_jobs_id_seq CASCADE;

DROP TABLE IF EXISTS gaussian_mixture_system_models CASCADE;
DROP SEQUENCE IF EXISTS gaussian_mixture_system_models_id_seq CASCADE;

DROP TABLE IF EXISTS tabular_policies CASCADE;
DROP SEQUENCE IF EXISTS tabular_policies_id_seq CASCADE;

DROP TABLE IF EXISTS alpha_vec_policies CASCADE;
DROP SEQUENCE IF EXISTS alpha_vec_policies_id_seq CASCADE;

DROP TABLE IF EXISTS dqn_policies CASCADE;
DROP SEQUENCE IF EXISTS dqn_policies_id_seq CASCADE;

DROP TABLE IF EXISTS fnn_w_softmax_policies CASCADE;
DROP SEQUENCE IF EXISTS fnn_w_softmax_policies_id_seq CASCADE;

DROP TABLE IF EXISTS vector_policies CASCADE;
DROP SEQUENCE IF EXISTS vector_policies_id_seq CASCADE;

DROP TABLE IF EXISTS emulation_executions CASCADE;

DROP TABLE IF EXISTS empirical_system_models CASCADE;
DROP SEQUENCE IF EXISTS empirical_system_models_id_seq CASCADE;

DROP TABLE IF EXISTS gp_system_models CASCADE;
DROP SEQUENCE IF EXISTS gp_system_models_id_seq CASCADE;

DROP TABLE IF EXISTS management_users CASCADE;
DROP SEQUENCE IF EXISTS management_users_id_seq CASCADE;

DROP TABLE IF EXISTS session_tokens CASCADE;

DROP TABLE IF EXISTS traces_datasets CASCADE;
DROP SEQUENCE IF EXISTS traces_datasets_id_seq CASCADE;

DROP TABLE IF EXISTS statistics_datasets CASCADE;
DROP SEQUENCE IF EXISTS statistics_datasets_id_seq CASCADE;

DROP TABLE IF EXISTS config CASCADE;

DROP TABLE IF EXISTS linear_threshold_stopping_policies CASCADE;
DROP SEQUENCE IF EXISTS linear_threshold_stopping_policies_id_seq CASCADE;

DROP TABLE IF EXISTS mcmc_system_models CASCADE;
DROP SEQUENCE IF EXISTS mcmc_system_models_id_seq CASCADE;