---
title: Metastore
permalink: /docs/metastore/
---

## Metastore

The metastore is a distributed relational database based on PostgreSQL and Citus. 
It stores metadata and management information about CSLE. 
This data includes: metadata about emulated IT infrastructures, 
metadata about reinforcement learning workloads, 
metadata about management users, metadata about simulation environments, 
and management information about virtual containers and networks 
(see Table 1 for a complete list).

The metastore is divided into N replicas. Each physical server of the management system stores one replica. 
Reads and writes to the metastore are distributed evenly across all replicas to maximize throughput. 
To coordinate writes and achieve consensus among replicas, a quorum-based two-phase commit (2PC) 
scheme is used. This means that the metastore tolerates N/2-1 failing replicas.

| *Table name*                        | *Description*                                    | *Columns*                                                   |
|-------------------------------------|--------------------------------------------------|-------------------------------------------------------------|
| `emulations`                        | Metadata about emulations.                       | `id`, `name`, `config`                                      |
| `emulations_traces`                 | Attack and system traces.                        | `id`, `emulation_name`, `trace`                             |
| `emulation_statistics`              | Count statistics of system metrics.              | `id`, `emulation_name`, `statistics`                        |
| `simulation_traces`                 | Simulation traces-                               | `id`, `gym_env`, `trace`                                    |
| `emulation_simulation_traces`       | Mapping between emulation and simulation traces. | `id`, `emulation_trace`, `simulation_trace`                 |
| `emulation_images`                  | Pictures of emulation topologies.                | `id`, `emulation_name`, `image`                             |
| `simulations`                       | Metadata about simulations.                      | `id`, `name`, `config`                                      |
| `experiment_executions`             | Metadata about experiments.                      | `id`, `execution`, `simulation_name`, `emulation_name`      |
| `simulation_images`                 | Pictures of simulations.                         | `id`, `simulation_name`, `image`                            |
| `multi_threshold_stopping_policies` | Threshold-based policies.                        | `id`, `policy`, `simulation_name`                           |
| `training_jobs`                     | Training jobs.                                   | `id`, `config`, `simulation_name`, `emulation_name`, `pid`  |
| `system_identification_jobs`        | System identification jobs.                      | `id`, `config`, `emulation_name`, `pid`                     |
| `ppo_policies`                      | PPO policies.                                    | `id`, `policy`, `simulation_name`                           |
| `system_models`                     | System models.                                   | `id`, `emulation_name`, `system_model`                      |
| `data_collection_jobs`              | Data collection jobs.                            | `id`, `config`, `emulation_name`, `pid`                     |
| `gaussian_mixture_system_models`    | Gaussian mixture system models.                  | `id`, `model`, `emulation_name`, `emulation_statistic_id`   |
| `tabular_policies`                  | Tabular policies.                                | `id`, `policy`, `simulation_name`                           |
| `alpha_vec_policies`                | Alpha vector policies.                           | `id`, `policy`, `simulation_name`                           |
| `dqn_policies`                      | DQN policies.                                    | `id`, `policy`, `simulation_name`                           |
| `fnn_w_softmax_policies`            | Feed-forward neural network policies.            | `id`, `policy`, `simulation_name`                           |
| `vector_policies`                   | Vector policies.                                 | `id`, `policy`, `simulation_name`                           |
| `emulation_executions`              | Emulation executions.                            | `ip_first_octet`, `emulation_name`, `info`                  |
| `empirical_system_models`           | Empirical system models.                         | `id`, `model`, `emulation_name`, `emulation_statistic_name` |
| `mcmc_system_models`                | MCMC system models.                              | `id`, `model`, `emulation_name`, `emulation_statistic_name` |
| `gp_system_models`                  | Gaussian process system models.                  | `id`, `model`, `emulation_name`, `emulation_statistic_id`   |
| `management_users`                  | Management users.                                | `id`, `username`, `password`, `email`, `first_name`, etc.   |
| `session_tokens`                    | Session tokens.                                  | `token`, `timestamp`, `username`                            |
| `traces_datasets`                   | Traces datasets.                                 | `id`, `name`, `description`, etc.                           |
| `statistics_datasets`               | Statistics datasets.                             | `id`, `name`, `description`, etc.                           |

<p class="captionFig">
Table 1: Metastore tables.
</p>