# `csle-rest-api`

A REST API for the CSLE management platform.

| resource                                                                 | description                                                 | Method                                  |
|:-------------------------------------------------------------------------|:------------------------------------------------------------|:----------------------------------------|
| `/emulations`                                                            | List of emulations                                          | `GET`,`DELETE`                          |
| `/emulations?ids=true`                                                   | List of emulation ids only (fast to fetch)                  | `GET`,`DELETE`                          |
| `/emulations/<emulation_id>`                                             | Individual  emulation                                       | `GET`,`DELETE`, `POST` (for start/stop) |
| `/emulations/<emulation_id>/executions`                                  | List of executions                                          | `GET`,`DELETE`                          |
| `/emulations/<emulation_id>/executions/<execution_id>`                   | Individual execution                                        | `GET`,`DELETE`                          |
| `/emulations/<emulation_id>/executions/<execution_id>/switches`          | List of SDN switches                                        | `GET`                                   |
| `/emulations/<emulation_id>/executions/<execution_id>/monitor/<minutes>` | Get last <minutes> of data from the execution               | `GET`                                   |
| `/emulations/<emulation_id>/executions/<execution_id>`                   | Individual execution                                        | `GET`,`DELETE`                          |
| `/simulations`                                                           | List of simulations                                         | `GET`,`DELETE`                          |
| `/simulations?id=true`                                                   | List of simulation ids only (fast to fetch)                 | `GET`,`DELETE`                          |
| `/simulations/<simulation_id>`                                           | Individual simulation                                       | `GET`,`DELETE`                          |
| `/cadvisor`                                                              | Starts/stops cadvisor                                       | `POST`                                  |
| `/nodeexporter`                                                          | Starts/stops nodeexporter                                   | `POST`                                  |
| `/grafana`                                                               | Starts/stops grafana                                        | `POST`                                  |
| `/prometheus`                                                            | Starts/stops prometheus                                     | `POST`                                  |
| `/alpha-vec-policies`                                                    | List of alpha vector policies                               | `GET`,`DELETE`                          |
| `/alpha-vec-policies?id=true`                                            | List of alpha vector policy ids only (fast to fetch)        | `GET`,`DELETE`                          |
| `/alpha-vec-policies/<policy_id>`                                        | Individual alpha vector policy                              | `GET`,`DELETE`                          |
| `/dqn-policies`                                                          | List of DQN policies                                        | `GET`,`DELETE`                          |
| `/dqn-policies?id=true`                                                  | List of DQN policy ids only (fast to fetch)                 | `GET`,`DELETE`                          |
| `/dqn-policies/<policy_id>`                                              | Individual DQN policy                                       | `GET`,`DELETE`                          |
| `/ppo-policies`                                                          | List of PPO policies                                        | `GET`,`DELETE`                          |
| `/ppo-policies?id=true`                                                  | List of PPO policy ids only (fast to fetch)                 | `GET`,`DELETE`                          |
| `/ppo-policies/<policy_id>`                                              | Individual PPO policy                                       | `GET`,`DELETE`                          |
| `/vector-policies`                                                       | List of vector policies                                     | `GET`,`DELETE`                          |
| `/vector-policies?id=true`                                               | List of vector policy ids only (fast to fetch)              | `GET`,`DELETE`                          |
| `/vector-policies/<policy_id>`                                           | Individual vector policy                                    | `GET`,`DELETE`                          |
| `/tabular-policies`                                                      | List of tabular policies                                    | `GET`,`DELETE`                          |
| `/tabular-policies?id=true`                                              | List of tabular policy ids only (fast to fetch)             | `GET`,`DELETE`                          |
| `/tabular-policies/<policy_id>`                                          | Individual tabular policy                                   | `GET`,`DELETE`                          |
| `/multi-threshold-policies`                                              | List of multi-threshold policies                            | `GET`,`DELETE`                          |
| `/multi-threshold-policies?id=true`                                      | List of multi-threshold policy ids only (fast to fetch)     | `GET`,`DELETE`                          |
| `/multi-threshold-policies/<policy_id>`                                  | Individual multi-threshold policy                           | `GET`,`DELETE`                          |
| `/fnn-w-softmax-policies`                                                | List of fnn-w-softmax policies                              | `GET`,`DELETE`                          |
| `/fnn-w-softmax-policies?id=true`                                        | List of fnn-w-softmax policy ids only (fast to fetch)       | `GET`,`DELETE`                          |
| `/fnn-w-softmax-policies/<policy_id>`                                    | Individual fnn-w-softmax policy                             | `GET`,`DELETE`                          |
| `/training-jobs`                                                         | List of training jobs                                       | `GET`,`DELETE`                          |
| `/training-jobs?id=true`                                                 | List of training job ids only (fast to fetch)               | `GET`,`DELETE`                          |
| `/training-jobs/<job_id>`                                                | Individual training job                                     | `GET`,`DELETE`, `POST` (for start/stop) |
| `/data-collection-jobs`                                                  | List of data-collection jobs                                | `GET`,`DELETE`                          |
| `/data-collection-jobs?id=true`                                          | List of data-collection job ids only (fast to fetch)        | `GET`,`DELETE`                          |
| `/data-collection-jobs/<job_id>`                                         | Individual data-collection job                              | `GET`,`DELETE`, `POST` (for start/stop) |
| `/system-identification-jobs`                                            | List of system-identification jobs                          | `GET`,`DELETE`                          |
| `/system-identification-jobs?id=true`                                    | List of system-identification job ids only (fast to fetch)  | `GET`,`DELETE`                          |
| `/system-identification-jobs/<job_id>`                                   | Individual system-identification job                        | `GET`,`DELETE`, `POST` (for start/stop) |
| `/emulation-traces`                                                      | List of emulation traces                                    | `GET`,`DELETE`                          |
| `/emulation-traces?id=true`                                              | List of emulation trace ids only (fast to fetch)            | `GET`,`DELETE`                          |
| `/emulation-traces/<trace_id>`                                           | Individual emulation trace                                  | `GET`,`DELETE`                          |
| `/simulation-traces`                                                     | List of simulation traces                                   | `GET`,`DELETE`                          |
| `/simulation-traces?id=true`                                             | List of simulation trace ids only (fast to fetch)           | `GET`,`DELETE`                          |
| `/simulation-traces/<trace_id>`                                          | Individual simulation trace                                 | `GET`,`DELETE`                          |
| `/emulation-simulation-traces`                                           | List of emulation-simulation traces                         | `GET`,`DELETE`                          |
| `/emulation-simulation-traces?id=true`                                   | List of emulation-simulation trace ids only (fast to fetch) | `GET`,`DELETE`                          |
| `/emulation-simulation-traces/<trace_id>`                                | Individual emulation-simulation trace                       | `GET`,`DELETE`                          |
| `/images`                                                                | List of Docker images                                       | `GET`                                   |
| `/file`                                                                  | Reads a given file from disk                                | `POST`                                  |
| `/experiments`                                                           | List of experiments                                         | `GET`,`DELETE`                          |
| `/experiments?id=true`                                                   | List of experiment ids only (fast to fetch)                 | `GET`,`DELETE`                          |
| `/experiments/<trace_id>`                                                | Individual experiment                                       | `GET`,`DELETE`                          |
| `/sdn-controllers`                                                       | List of SDN controllers                                     | `GET`,`DELETE`                          |
| `/sdn-controllers?id=true`                                               | List of SDN controller ids only (fast to fetch)             | `GET`,`DELETE`                          |
| `/emulation-statistics`                                                  | List of emulation statistics                                | `GET`,`DELETE`                          |
| `/emulation-statistics?id=true`                                          | List of emulation statistic ids only (fast to fetch)        | `GET`,`DELETE`                          |
| `/emulation-statistics/<trace_id>`                                       | Individual emulation statistic                              | `GET`,`DELETE`                          |
| `/system-models`                                                         | List of system-models                                       | `GET`,`DELETE`                          |
| `/system-models?id=true`                                                 | List of system-model ids only (fast to fetch)               | `GET`,`DELETE`                          |
| `/system-models/<trace_id>`                                              | Individual system model                                     | `GET`,`DELETE`                          |

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

Creative Commons

[LICENSE](../../LICENSE.md)

(C) 2020-2022, Kim Hammar

