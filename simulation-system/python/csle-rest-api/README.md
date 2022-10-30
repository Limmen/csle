# `csle-rest-api`

A REST API for the CSLE management platform.

| resource                                                                                           | description                                                    | Method                                  |
|:---------------------------------------------------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------|
| `/emulations`                                                                                      | List of emulations                                             | `GET`,`DELETE`                          |
| `/emulations?ids=true&token=<valid_token>`                                                         | List of emulation ids only (fast to fetch)                     | `GET`,`DELETE`                          |
| `/emulations/<emulation_id>?token=<valid_token>`                                                   | Individual  emulation                                          | `GET`,`DELETE`, `POST` (for start/stop) |
| `/emulations/<emulation_id>/executions?token=<valid_token>`                                        | List of executions                                             | `GET`,`DELETE`                          |
| `/emulations/<emulation_id>/executions/<execution_id>?token=<valid_token>`                         | Individual execution                                           | `GET`,`DELETE`                          |
| `/emulations/<emulation_id>/executions/<execution_id>/switches?token=<valid_token>`                | List of SDN switches                                           | `GET`                                   |
| `/emulations/<emulation_id>/executions/<execution_id>/monitor/<minutes>?token=<valid_token>`       | Get last <minutes> of data from the execution                  | `GET`                                   |
| `/emulations/<emulation_id>/executions/<execution_id>?token=<valid_token>`                         | Individual execution                                           | `GET`,`DELETE`                          |
| `/simulations?token=<valid_token>`                                                                 | List of simulations                                            | `GET`,`DELETE`                          |
| `/simulations?ids=true&token=<valid_token>`                                                        | List of simulation ids only (fast to fetch)                    | `GET`,`DELETE`                          |
| `/simulations/<simulation_id>?token=<valid_token>`                                                 | Individual simulation                                          | `GET`,`DELETE`                          |
| `/cadvisor?token=<valid_token>`                                                                    | Starts/stops cadvisor                                          | `POST`                                  |
| `/nodeexporter?token=<valid_token>`                                                                | Starts/stops nodeexporter                                      | `POST`                                  |
| `/grafana?token=<valid_token>`                                                                     | Starts/stops grafana                                           | `POST`                                  |
| `/prometheus?token=<valid_token>`                                                                  | Starts/stops prometheus                                        | `POST`                                  |
| `/alpha-vec-policies?token=<valid_token>`                                                          | List of alpha vector policies                                  | `GET`,`DELETE`                          |
| `/alpha-vec-policies?ids=true&token=<valid_token>`                                                 | List of alpha vector policy ids only (fast to fetch)           | `GET`,`DELETE`                          |
| `/alpha-vec-policies/<policy_id>?token=<valid_token>`                                              | Individual alpha vector policy                                 | `GET`,`DELETE`                          |
| `/dqn-policies?token=<valid_token>`                                                                | List of DQN policies                                           | `GET`,`DELETE`                          |
| `/dqn-policies?ids=true&token=<valid_token>`                                                       | List of DQN policy ids only (fast to fetch)                    | `GET`,`DELETE`                          |
| `/dqn-policies/<policy_id>?token=<valid_token>`                                                    | Individual DQN policy                                          | `GET`,`DELETE`                          |
| `/ppo-policies?token=<valid_token>`                                                                | List of PPO policies                                           | `GET`,`DELETE`                          |
| `/ppo-policies?ids=true&token=<valid_token>`                                                       | List of PPO policy ids only (fast to fetch)                    | `GET`,`DELETE`                          |
| `/ppo-policies/<policy_id>?token=<valid_token>`                                                    | Individual PPO policy                                          | `GET`,`DELETE`                          |
| `/vector-policies?token=<valid_token>`                                                             | List of vector policies                                        | `GET`,`DELETE`                          |
| `/vector-policies?ids=true&token=<valid_token>`                                                    | List of vector policy ids only (fast to fetch)                 | `GET`,`DELETE`                          |
| `/vector-policies/<policy_id>?token=<valid_token>`                                                 | Individual vector policy                                       | `GET`,`DELETE`                          |
| `/tabular-policies?token=<valid_token>`                                                            | List of tabular policies                                       | `GET`,`DELETE`                          |
| `/tabular-policies?ids=true&token=<valid_token>`                                                   | List of tabular policy ids only (fast to fetch)                | `GET`,`DELETE`                          |
| `/tabular-policies/<policy_id>?token=<valid_token>`                                                | Individual tabular policy                                      | `GET`,`DELETE`                          |
| `/multi-threshold-policies?token=<valid_token>`                                                    | List of multi-threshold policies                               | `GET`,`DELETE`                          |
| `/multi-threshold-policies?ids=true&token=<valid_token>`                                           | List of multi-threshold policy ids only (fast to fetch)        | `GET`,`DELETE`                          |
| `/multi-threshold-policies/<policy_id>?token=<valid_token>`                                        | Individual multi-threshold policy                              | `GET`,`DELETE`                          |
| `/fnn-w-softmax-policies?token=<valid_token>`                                                      | List of fnn-w-softmax policies                                 | `GET`,`DELETE`                          |
| `/fnn-w-softmax-policies?ids=true&token=<valid_token>`                                             | List of fnn-w-softmax policy ids only (fast to fetch)          | `GET`,`DELETE`                          |
| `/fnn-w-softmax-policies/<policy_id>?token=<valid_token>`                                          | Individual fnn-w-softmax policy                                | `GET`,`DELETE`                          |
| `/training-jobs?token=<valid_token>`                                                               | List of training jobs                                          | `GET`,`DELETE`                          |
| `/training-jobs?ids=true&token=<valid_token>`                                                      | List of training job ids only (fast to fetch)                  | `GET`,`DELETE`                          |
| `/training-jobs/<job_id>?token=<valid_token>`                                                      | Individual training job                                        | `GET`,`DELETE`, `POST` (for start/stop) |
| `/data-collection-jobs?token=<valid_token>`                                                        | List of data-collection jobs                                   | `GET`,`DELETE`                          |
| `/data-collection-jobs?ids=true&token=<valid_token>`                                               | List of data-collection job ids only (fast to fetch)           | `GET`,`DELETE`                          |
| `/data-collection-jobs/<job_id>?token=<valid_token>`                                               | Individual data-collection job                                 | `GET`,`DELETE`, `POST` (for start/stop) |
| `/system-identification-jobs?token=<valid_token>`                                                  | List of system-identification jobs                             | `GET`,`DELETE`                          |
| `/system-identification-jobs?ids=true&token=<valid_token>`                                         | List of system-identification job ids only (fast to fetch)     | `GET`,`DELETE`                          |
| `/system-identification-jobs/<job_id>?token=<valid_token>`                                         | Individual system-identification job                           | `GET`,`DELETE`, `POST` (for start/stop) |
| `/emulation-traces?token=<valid_token>`                                                            | List of emulation traces                                       | `GET`,`DELETE`                          |
| `/emulation-traces?ids=true&token=<valid_token>`                                                   | List of emulation trace ids only (fast to fetch)               | `GET`,`DELETE`                          |
| `/emulation-traces/<trace_id>?token=<valid_token>`                                                 | Individual emulation trace                                     | `GET`,`DELETE`                          |
| `/simulation-traces?token=<valid_token>`                                                           | List of simulation traces                                      | `GET`,`DELETE`                          |
| `/simulation-traces?ids=true&token=<valid_token>`                                                  | List of simulation trace ids only (fast to fetch)              | `GET`,`DELETE`                          |
| `/simulation-traces/<trace_id>?token=<valid_token>`                                                | Individual simulation trace                                    | `GET`,`DELETE`                          |
| `/emulation-simulation-traces?token=<valid_token>`                                                 | List of emulation-simulation traces                            | `GET`,`DELETE`                          |
| `/emulation-simulation-traces?ids=true&token=<valid_token>`                                        | List of emulation-simulation trace ids only (fast to fetch)    | `GET`,`DELETE`                          |
| `/emulation-simulation-traces/<trace_id>?token=<valid_token>`                                      | Individual emulation-simulation trace                          | `GET`,`DELETE`                          |
| `/images?token=<valid_token>`                                                                      | List of Docker images                                          | `GET`                                   |
| `/file?token=<valid_token>`                                                                        | Reads a given file from disk                                   | `POST`                                  |
| `/experiments?token=<valid_token>`                                                                 | List of experiments                                            | `GET`,`DELETE`                          |
| `/experiments?ids=true&token=<valid_token>`                                                        | List of experiment ids only (fast to fetch)                    | `GET`,`DELETE`                          |
| `/experiments/<trace_id>?token=<valid_token>`                                                      | Individual experiment                                          | `GET`,`DELETE`                          |
| `/sdn-controllers?token=<valid_token>`                                                             | List of SDN controllers                                        | `GET`,`DELETE`                          |
| `/sdn-controllers?ids=true&token=<valid_token>`                                                    | List of SDN controller ids only (fast to fetch)                | `GET`,`DELETE`                          |
| `/emulation-statistics?token=<valid_token>`                                                        | List of emulation statistics                                   | `GET`,`DELETE`                          |
| `/emulation-statistics?ids=true&token=<valid_token>`                                               | List of emulation statistic ids only (fast to fetch)           | `GET`,`DELETE`                          |
| `/emulation-statistics/<trace_id>?token=<valid_token>`                                             | Individual emulation statistic                                 | `GET`,`DELETE`                          |
| `/gaussian-mixture-system-models?token=<valid_token>`                                              | List of gaussian mixture system-models                         | `GET`,`DELETE`                          |
| `/gaussian-mixture-system-models?ids=true&token=<valid_token>`                                     | List of gaussian mixture system-model ids only (fast to fetch) | `GET`,`DELETE`                          |
| `/gaussian-mixture-system-models/<trace_id>?token=<valid_token>`                                   | Individual gaussian mixture system model                       | `GET`,`DELETE`                          |
| `/empirical-system-models?token=<valid_token>`                                                     | List of empirical system-models                                | `GET`,`DELETE`                          |
| `/empirical-system-models?ids=true&token=<valid_token>`                                            | List of empirical system-model ids only (fast to fetch)        | `GET`,`DELETE`                          |
| `/empirical-system-models/<trace_id>?token=<valid_token>`                                          | Individual empirical system model                              | `GET`,`DELETE`                          |
| `/gp-system-models?token=<valid_token>`                                                            | List of gp system-models                                       | `GET`,`DELETE`                          |
| `/gp-system-models?ids=true&token=<valid_token>`                                                   | List of gp system-model ids only (fast to fetch)               | `GET`,`DELETE`                          |
| `/gp-system-models/<trace_id>?token=<valid_token>`                                                 | Individual gp system model                                     | `GET`,`DELETE`                          |
| `/system-models?ids=true&token=<valid_token>`                                                      | List of all system model ids (fast to fetch)                   | `GET`                                   |
| `/login`                                                                                           | Login and generate new token (credentials as payload)          | `POST`                                  |
| `/traces-datasets?token=<valid_token>`                                                             | List of traces datasets                                        | `GET`,`DELETE`                          |
| `/traces-datasets?ids=true&token=<valid_token>`                                                    | List of traces datasets ids only (fast to fetch)               | `GET`,`DELETE`                          |
| `/traces-datasets/<traces_datasets_id>?token=<valid_token>`                                        | Individual traces dataset                                      | `GET`,`DELETE`                          |
| `/traces-datasets/<traces_datasets_id>?token=<valid_token>&download=true`                          | Downloads and individual traces dataset                        | `GET`                                   |
| `/statistics-datasets?token=<valid_token>`                                                         | List of statistics datasets                                    | `GET`,`DELETE`                          |
| `/statistics-datasets?ids=true&token=<valid_token>`                                                | List of statistics datasets ids only (fast to fetch)           | `GET`,`DELETE`                          |
| `/statistics-datasets/<statistics_datasets_id>?token=<valid_token>`                                | Individual statistics dataset                                  | `GET`,`DELETE`                          |
| `/statistics-datasets/<statistics_datasets_id>?token=<valid_token>&download=true`                  | Downloads and individual statistics dataset                    | `GET`                                   |
| `/emulation-executions?token=<valid_token>`                                                        | List of emulation executions                                   | `GET`,`DELETE`                          |
| `/emulation-executions?ids=true&token=<valid_token>`                                               | List of emulation execution ids only (fast to fetch)           | `GET`,`DELETE`                          |
| `/emulation-executions/<execution_id>?token=<valid_token>`                                         | Individual emulation execution                                 | `GET`,`DELETE`                          |
| `/emulation-executions/<execution_id>/info?token=<valid_token>&emulation=<emulation>`              | Runtime information about an emulation execution               | `GET`                                   |
| `/emulation-executions/<execution_id>/client-manager?token=<valid_token>&emulation=<emulation>`    | Start/stop client manager of an emulation execution            | `POST`                                  |
| `/emulation-executions/<execution_id>/kafka-manager?token=<valid_token>&emulation=<emulation>`     | Start/stop Kafka manager of an emulation execution             | `POST`                                  |
| `/emulation-executions/<execution_id>/snort-ids-manager?token=<valid_token>&emulation=<emulation>` | Start/stop Snort manager of an emulation execution             | `POST`                                  |
| `/emulation-executions/<execution_id>/ossec-ids-manager?token=<valid_token>&emulation=<emulation>` | Start/stop OSSEC IDS manager of an emulation execution         | `POST`                                  |
| `/emulation-executions/<execution_id>/host-manager?token=<valid_token>&emulation=<emulation>`      | Start/stop Host managers of an emulation execution             | `POST`                                  |
| `/emulation-executions/<execution_id>/container?token=<valid_token>&emulation=<emulation>`         | Start/stop container of an emulation execution                  | `POST`                                  |

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2020-2022, Kim Hammar

