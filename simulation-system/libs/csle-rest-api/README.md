# `csle-rest-api`

A REST API for the CSLE management platform.

[![PyPI version](https://badge.fury.io/py/csle-rest-api.svg)](https://badge.fury.io/py/csle-rest-api)
![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-rest-api)

## Endpoints

| resource                                                                                              | description                                                    | Method                                  |
|:------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------|
| `/emulations`                                                                                         | List of emulations                                             | `GET`,`DELETE`                          |
| `/emulations?ids=true&token=<valid_token>`                                                            | List of emulation ids only (fast to fetch)                     | `GET`,`DELETE`                          |
| `/emulations/<emulation_id>?token=<valid_token>`                                                      | Individual  emulation                                          | `GET`,`DELETE`, `POST` (for start/stop) |
| `/emulations/<emulation_id>/executions?token=<valid_token>`                                           | List of executions                                             | `GET`,`DELETE`                          |
| `/emulations/<emulation_id>/executions/<execution_id>?token=<valid_token>`                            | Individual execution                                           | `GET`,`DELETE`                          |
| `/emulations/<emulation_id>/executions/<execution_id>/monitor/<minutes>?token=<valid_token>`          | Get last X minutes of data from an execution                   | `GET`                                   |
| `/simulations?token=<valid_token>`                                                                    | List of simulations                                            | `GET`,`DELETE`                          |
| `/simulations?ids=true&token=<valid_token>`                                                           | List of simulation ids only (fast to fetch)                    | `GET`,`DELETE`                          |
| `/simulations/<simulation_id>?token=<valid_token>`                                                    | Individual simulation                                          | `GET`,`DELETE`                          |
| `/cadvisor?token=<valid_token>`                                                                       | Starts/stops or gets status cadvisor                           | `GET`,`POST`                            |
| `/pgadmin?token=<valid_token>`                                                                        | Starts/stops or gets status of pgadmin                         | `GET`,`POST`                            |
| `/nodeexporter?token=<valid_token>`                                                                   | Starts/stops or gets status of nodeexporter                    | `GET`,`POST`                            |
| `/grafana?token=<valid_token>`                                                                        | Starts/stops or gets status of grafana                         | `GET`, `POST`                           |
| `/clusterstatuses?token=<valid_token>`                                                                | Gets the status of management services of the cluster          | `GET`                                   |
| `/prometheus?token=<valid_token>`                                                                     | Starts/stops or gets status of prometheus                      | `GET`,`POST`                            |
| `/postgresql?token=<valid_token>`                                                                     | Starts/stops or gets status of postgresql                      | `GET`,`POST`                            |
| `/docker?token=<valid_token>`                                                                         | Starts/stops or gets status of docker engine                   | `GET`,`POST`                            |
| `/nginx?token=<valid_token>`                                                                          | Starts/stops or gets status of nginx                           | `GET`,`POST`                            |
| `/flask?token=<valid_token>`                                                                          | Starts/stops or gets status of flask                           | `GET`,`POST`                            |
| `/alpha-vec-policies?token=<valid_token>`                                                             | List of alpha vector policies                                  | `GET`,`DELETE`                          |
| `/alpha-vec-policies?ids=true&token=<valid_token>`                                                    | List of alpha vector policy ids only (fast to fetch)           | `GET`,`DELETE`                          |
| `/alpha-vec-policies/<policy_id>?token=<valid_token>`                                                 | Individual alpha vector policy                                 | `GET`,`DELETE`                          |
| `/dqn-policies?token=<valid_token>`                                                                   | List of DQN policies                                           | `GET`,`DELETE`                          |
| `/dqn-policies?ids=true&token=<valid_token>`                                                          | List of DQN policy ids only (fast to fetch)                    | `GET`,`DELETE`                          |
| `/dqn-policies/<policy_id>?token=<valid_token>`                                                       | Individual DQN policy                                          | `GET`,`DELETE`                          |
| `/ppo-policies?token=<valid_token>`                                                                   | List of PPO policies                                           | `GET`,`DELETE`                          |
| `/ppo-policies?ids=true&token=<valid_token>`                                                          | List of PPO policy ids only (fast to fetch)                    | `GET`,`DELETE`                          |
| `/ppo-policies/<policy_id>?token=<valid_token>`                                                       | Individual PPO policy                                          | `GET`,`DELETE`                          |
| `/vector-policies?token=<valid_token>`                                                                | List of vector policies                                        | `GET`,`DELETE`                          |
| `/vector-policies?ids=true&token=<valid_token>`                                                       | List of vector policy ids only (fast to fetch)                 | `GET`,`DELETE`                          |
| `/vector-policies/<policy_id>?token=<valid_token>`                                                    | Individual vector policy                                       | `GET`,`DELETE`                          |
| `/tabular-policies?token=<valid_token>`                                                               | List of tabular policies                                       | `GET`,`DELETE`                          |
| `/tabular-policies?ids=true&token=<valid_token>`                                                      | List of tabular policy ids only (fast to fetch)                | `GET`,`DELETE`                          |
| `/tabular-policies/<policy_id>?token=<valid_token>`                                                   | Individual tabular policy                                      | `GET`,`DELETE`                          |
| `/multi-threshold-policies?token=<valid_token>`                                                       | List of multi-threshold policies                               | `GET`,`DELETE`                          |
| `/multi-threshold-policies?ids=true&token=<valid_token>`                                              | List of multi-threshold policy ids only (fast to fetch)        | `GET`,`DELETE`                          |
| `/multi-threshold-policies/<policy_id>?token=<valid_token>`                                           | Individual multi-threshold policy                              | `GET`,`DELETE`                          |
| `/linear-threshold-policies?token=<valid_token>`                                                      | List of linear threshold policies                              | `GET`,`DELETE`                          |
| `/linear-threshold-policies?ids=true&token=<valid_token>`                                             | List of linear threshold policy ids only (fast to fetch)       | `GET`,`DELETE`                          |
| `/linear-threshold-policies/<policy_id>?token=<valid_token>`                                          | Individual linear threshold policy                             | `GET`,`DELETE`                          |
| `/fnn-w-softmax-policies?token=<valid_token>`                                                         | List of fnn-w-softmax policies                                 | `GET`,`DELETE`                          |
| `/fnn-w-softmax-policies?ids=true&token=<valid_token>`                                                | List of fnn-w-softmax policy ids only (fast to fetch)          | `GET`,`DELETE`                          |
| `/fnn-w-softmax-policies/<policy_id>?token=<valid_token>`                                             | Individual fnn-w-softmax policy                                | `GET`,`DELETE`                          |
| `/training-jobs?token=<valid_token>`                                                                  | List of training jobs                                          | `GET`,`DELETE`                          |
| `/training-jobs?ids=true&token=<valid_token>`                                                         | List of training job ids only (fast to fetch)                  | `GET`,`DELETE`                          |
| `/training-jobs/<job_id>?token=<valid_token>`                                                         | Individual training job                                        | `GET`,`DELETE`, `POST` (for start/stop) |
| `/data-collection-jobs?token=<valid_token>`                                                           | List of data-collection jobs                                   | `GET`,`DELETE`                          |
| `/data-collection-jobs?ids=true&token=<valid_token>`                                                  | List of data-collection job ids only (fast to fetch)           | `GET`,`DELETE`                          |
| `/data-collection-jobs/<job_id>?token=<valid_token>`                                                  | Individual data-collection job                                 | `GET`,`DELETE`, `POST` (for start/stop) |
| `/system-identification-jobs?token=<valid_token>`                                                     | List of system-identification jobs                             | `GET`,`DELETE`                          |
| `/system-identification-jobs?ids=true&token=<valid_token>`                                            | List of system-identification job ids only (fast to fetch)     | `GET`,`DELETE`                          |
| `/system-identification-jobs/<job_id>?token=<valid_token>`                                            | Individual system-identification job                           | `GET`,`DELETE`, `POST` (for start/stop) |
| `/emulation-traces?token=<valid_token>`                                                               | List of emulation traces                                       | `GET`,`DELETE`                          |
| `/emulation-traces?ids=true&token=<valid_token>`                                                      | List of emulation trace ids only (fast to fetch)               | `GET`,`DELETE`                          |
| `/emulation-traces/<trace_id>?token=<valid_token>`                                                    | Individual emulation trace                                     | `GET`,`DELETE`                          |
| `/simulation-traces?token=<valid_token>`                                                              | List of simulation traces                                      | `GET`,`DELETE`                          |
| `/simulation-traces?ids=true&token=<valid_token>`                                                     | List of simulation trace ids only (fast to fetch)              | `GET`,`DELETE`                          |
| `/simulation-traces/<trace_id>?token=<valid_token>`                                                   | Individual simulation trace                                    | `GET`,`DELETE`                          |
| `/emulation-simulation-traces?token=<valid_token>`                                                    | List of emulation-simulation traces                            | `GET`,`DELETE`                          |
| `/emulation-simulation-traces?ids=true&token=<valid_token>`                                           | List of emulation-simulation trace ids only (fast to fetch)    | `GET`,`DELETE`                          |
| `/emulation-simulation-traces/<trace_id>?token=<valid_token>`                                         | Individual emulation-simulation trace                          | `GET`,`DELETE`                          |
| `/images?token=<valid_token>`                                                                         | List of Docker images                                          | `GET`                                   |
| `/file?token=<valid_token>`                                                                           | Reads a given file from disk                                   | `POST`                                  |
| `/experiments?token=<valid_token>`                                                                    | List of experiments                                            | `GET`,`DELETE`                          |
| `/experiments?ids=true&token=<valid_token>`                                                           | List of experiment ids only (fast to fetch)                    | `GET`,`DELETE`                          |
| `/experiments/<trace_id>?token=<valid_token>`                                                         | Individual experiment                                          | `GET`,`DELETE`                          |
| `/sdn-controllers?token=<valid_token>`                                                                | List of SDN controllers                                        | `GET`,`DELETE`                          |
| `/sdn-controllers?ids=true&token=<valid_token>`                                                       | List of SDN controller ids only (fast to fetch)                | `GET`,`DELETE`                          |
| `/emulation-statistics?token=<valid_token>`                                                           | List of emulation statistics                                   | `GET`,`DELETE`                          |
| `/emulation-statistics?ids=true&token=<valid_token>`                                                  | List of emulation statistic ids only (fast to fetch)           | `GET`,`DELETE`                          |
| `/emulation-statistics/<trace_id>?token=<valid_token>`                                                | Individual emulation statistic                                 | `GET`,`DELETE`                          |
| `/gaussian-mixture-system-models?token=<valid_token>`                                                 | List of gaussian mixture system-models                         | `GET`,`DELETE`                          |
| `/gaussian-mixture-system-models?ids=true&token=<valid_token>`                                        | List of gaussian mixture system-model ids only (fast to fetch) | `GET`,`DELETE`                          |
| `/gaussian-mixture-system-models/<trace_id>?token=<valid_token>`                                      | Individual gaussian mixture system model                       | `GET`,`DELETE`                          |
| `/empirical-system-models?token=<valid_token>`                                                        | List of empirical system-models                                | `GET`,`DELETE`                          |
| `/empirical-system-models?ids=true&token=<valid_token>`                                               | List of empirical system-model ids only (fast to fetch)        | `GET`,`DELETE`                          |
| `/empirical-system-models/<trace_id>?token=<valid_token>`                                             | Individual empirical system model                              | `GET`,`DELETE`                          |
| `/mcmc-system-models?token=<valid_token>`                                                             | List of mcmc system-models                                     | `GET`,`DELETE`                          |
| `/mcmc-system-models?ids=true&token=<valid_token>`                                                    | List of mcmc system-model ids only (fast to fetch)             | `GET`,`DELETE`                          |
| `/mcmc-system-models/<trace_id>?token=<valid_token>`                                                  | Individual mcmc system model                                   | `GET`,`DELETE`                          |
| `/gp-system-models?token=<valid_token>`                                                               | List of gp system-models                                       | `GET`,`DELETE`                          |
| `/gp-system-models?ids=true&token=<valid_token>`                                                      | List of gp system-model ids only (fast to fetch)               | `GET`,`DELETE`                          |
| `/gp-system-models/<model_id>?token=<valid_token>`                                                    | Individual gp system model                                     | `GET`,`DELETE`                          |
| `/system-models?ids=true&token=<valid_token>`                                                         | List of all system model ids (fast to fetch)                   | `GET`                                   |
| `/login`                                                                                              | Login and generate new token (credentials as payload)          | `POST`                                  |
| `/traces-datasets?token=<valid_token>`                                                                | List of traces datasets                                        | `GET`,`DELETE`                          |
| `/traces-datasets?ids=true&token=<valid_token>`                                                       | List of traces datasets ids only (fast to fetch)               | `GET`,`DELETE`                          |
| `/traces-datasets/<traces_datasets_id>?token=<valid_token>`                                           | Individual traces dataset                                      | `GET`,`DELETE`                          |
| `/traces-datasets/<traces_datasets_id>?token=<valid_token>&download=true`                             | Downloads and individual traces dataset                        | `GET`                                   |
| `/statistics-datasets?token=<valid_token>`                                                            | List of statistics datasets                                    | `GET`,`DELETE`                          |
| `/statistics-datasets?ids=true&token=<valid_token>`                                                   | List of statistics datasets ids only (fast to fetch)           | `GET`,`DELETE`                          |
| `/statistics-datasets/<statistics_datasets_id>?token=<valid_token>`                                   | Individual statistics dataset                                  | `GET`,`DELETE`                          |
| `/statistics-datasets/<statistics_datasets_id>?token=<valid_token>&download=true`                     | Downloads and individual statistics dataset                    | `GET`                                   |
| `/emulation-executions?token=<valid_token>`                                                           | List of emulation executions                                   | `GET`,`DELETE`                          |
| `/emulation-executions?ids=true&token=<valid_token>`                                                  | List of emulation execution ids only (fast to fetch)           | `GET`,`DELETE`                          |
| `/emulation-executions/<execution_id>?token=<valid_token>`                                            | Individual emulation execution                                 | `GET`,`DELETE`                          |
| `/emulation-executions/<execution_id>/info?token=<valid_token>&emulation=<emulation>`                 | Runtime information about an emulation execution               | `GET`                                   |
| `/emulation-executions/<execution_id>/docker-stats-manager?token=<valid_token>&emulation=<emulation>` | Start/stop docker stats manager of an emulation execution      | `POST`                                  |
| `/emulation-executions/<execution_id>/docker-stats-monitor?token=<valid_token>&emulation=<emulation>` | Start/stop docker stats monitor of an emulation execution      | `POST`                                  |
| `/emulation-executions/<execution_id>/client-manager?token=<valid_token>&emulation=<emulation>`       | Start/stop client manager of an emulation execution            | `POST`                                  |
| `/emulation-executions/<execution_id>/client-population?token=<valid_token>&emulation=<emulation>`    | Start/stop client population of an emulation execution         | `POST`                                  |
| `/emulation-executions/<execution_id>/client-producer?token=<valid_token>&emulation=<emulation>`      | Start/stop client producer of an emulation execution           | `POST`                                  |
| `/emulation-executions/<execution_id>/kafka-manager?token=<valid_token>&emulation=<emulation>`        | Start/stop Kafka manager of an emulation execution             | `POST`                                  |
| `/emulation-executions/<execution_id>/kafka?token=<valid_token>&emulation=<emulation>`                | Start/stop Kafka of an emulation execution                     | `POST`                                  |
| `/emulation-executions/<execution_id>/snort-ids-manager?token=<valid_token>&emulation=<emulation>`    | Start/stop Snort manager of an emulation execution             | `POST`                                  |
| `/emulation-executions/<execution_id>/snort-ids-monitor?token=<valid_token>&emulation=<emulation>`    | Start/stop Snort monitor of an emulation execution             | `POST`                                  |
| `/emulation-executions/<execution_id>/snort-ids?token=<valid_token>&emulation=<emulation>`            | Start/stop Snort on an emulation execution                     | `POST`                                  |
| `/emulation-executions/<execution_id>/ossec-ids-manager?token=<valid_token>&emulation=<emulation>`    | Start/stop OSSEC IDS manager of an emulation execution         | `POST`                                  |
| `/emulation-executions/<execution_id>/ossec-ids?token=<valid_token>&emulation=<emulation>`            | Start/stop OSSEC IDS of an emulation execution                 | `POST`                                  |
| `/emulation-executions/<execution_id>/ossec-ids-monitor?token=<valid_token>&emulation=<emulation>`    | Start/stop OSSEC IDS monitor of an emulation execution         | `POST`                                  |
| `/emulation-executions/<execution_id>/host-manager?token=<valid_token>&emulation=<emulation>`         | Start/stop Host managers of an emulation execution             | `POST`                                  |
| `/emulation-executions/<execution_id>/host-monitor?token=<valid_token>&emulation=<emulation>`         | Start/stop Host monitors of an emulation execution             | `POST`                                  |
| `/emulation-executions/<execution_id>/elk-manager?token=<valid_token>&emulation=<emulation>`          | Start/stop ELK managers of an emulation execution              | `POST`                                  |
| `/emulation-executions/<execution_id>/elastic?token=<valid_token>&emulation=<emulation>`              | Start/stop Elasticsearch on an emulation execution             | `POST`                                  |
| `/emulation-executions/<execution_id>/logstash?token=<valid_token>&emulation=<emulation>`             | Start/stop Logstash on an emulation execution                  | `POST`                                  |
| `/emulation-executions/<execution_id>/kibana?token=<valid_token>&emulation=<emulation>`               | Start/stop Kibana on an emulation execution                    | `POST`                                  |
| `/emulation-executions/<execution_id>/container?token=<valid_token>&emulation=<emulation>`            | Start/stop container of an emulation execution                 | `POST`                                  |
| `/emulation-executions/<execution_id>/elk-stack?token=<valid_token>&emulation=<emulation>`            | Start/stop ELK stack of an emulation execution                 | `POST`                                  |
| `/emulation-executions/<execution_id>/traffic-generator?token=<valid_token>&emulation=<emulation>`    | Start/stop traffic generators of an emulation execution        | `POST`                                  |
| `/emulation-executions/<execution_id>/filebeat?token=<valid_token>&emulation=<emulation>`             | Start/stop filebeats of an emulation execution                 | `POST`                                  |
| `/emulation-executions/<execution_id>/packetbeat?token=<valid_token>&emulation=<emulation>`           | Start/stop packetbeats of an emulation execution               | `POST`                                  |
| `/emulation-executions/<execution_id>/metricbeat?token=<valid_token>&emulation=<emulation>`           | Start/stop metricbeats of an emulation execution               | `POST`                                  |
| `/emulation-executions/<execution_id>/ryu-manager?token=<valid_token>&emulation=<emulation>`          | Start/stop ryu manager of an emulation execution               | `POST`                                  |
| `/emulation-executions/<execution_id>/ryu-monitor?token=<valid_token>&emulation=<emulation>`          | Start/stop ryu monitor of an emulation execution               | `POST`                                  |
| `/emulation-executions/<execution_id>/ryu-controller?token=<valid_token>&emulation=<emulation>`       | Start/stop ryu controller of an emulation execution            | `POST`                                  |
| `/emulation-executions/<execution_id>/switches?token=<valid_token>&emulation=<emulation>`             | List of SDN switches                                           | `GET`                                   |
| `/users?token=<valid_token>`                                                                          | Get/Update/Delete List of users                                | `GET`,`DELETE`, `PUT`                   |
| `/users?ids=true&token=<valid_token>`                                                                 | List of user ids only (fast to fetch)                          | `GET`,`DELETE`                          |
| `/users/<user_id>?token=<valid_token>`                                                                | Get/update/delete individual user                              | `GET`,`DELETE`, `PUT`                   |
| `/users/create`                                                                                       | Create a new user                                              | `POST`                                  |
| `/logs?token=<valid_token>`                                                                           | Get list of log files from the log dir                         | `GET`                                   |
| `/logs/docker-stats-manager?token=<valid_token>`                                                      | Get logs of the docker stats manager                           | `GET`                                   |
| `/logs/prometheus?token=<valid_token>`                                                                | Get logs of Prometheus                                         | `GET`                                   |
| `/logs/grafana?token=<valid_token>`                                                                   | Get logs of Grafana                                            | `GET`                                   |
| `/logs/nginx?token=<valid_token>`                                                                     | Get logs of Nginx                                              | `GET`                                   |
| `/logs/postgresql?token=<valid_token>`                                                                | Get logs of PostgreSQL                                         | `GET`                                   |
| `/logs/docker?token=<valid_token>`                                                                    | Get logs of Docker engine                                      | `GET`                                   |
| `/logs/flask?token=<valid_token>`                                                                     | Get logs of Flask                                              | `GET`                                   |
| `/logs/clustermanager?token=<valid_token>`                                                            | Get logs of the Cluster manager                                | `GET`                                   |
| `/logs/cadvisor?token=<valid_token>`                                                                  | Get logs of CAdvisor                                           | `GET`                                   |
| `/logs/pgadmin?token=<valid_token>`                                                                   | Get logs of pgAdmin                                            | `GET`                                   |
| `/logs/container?token=<valid_token>&container=<container_name>`                                      | Get logs of a specific container                               | `POST`                                  |
| `/logs/node-exporter?token=<valid_token>`                                                             | Get logs of node-exporter                                      | `GET`                                   |
| `/logs/client-manager?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`      | Get logs of a specific client manager                          | `POST`                                  |
| `/logs/kafka-manager?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`       | Get logs of a specific Kafka manager                           | `POST`                                  |
| `/logs/elk-manager?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`         | Get logs of a specific ELK manager                             | `POST`                                  |
| `/logs/ryu-manager?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`         | Get logs of a specific Ryu manager                             | `POST`                                  |
| `/logs/traffic-manager?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`     | Get logs of a specific traffic manager                         | `POST`                                  |
| `/logs/snort-ids-manager?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`   | Get logs of a specific Snort IDS manager                       | `POST`                                  |
| `/logs/ossec-ids-manager?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`   | Get logs of a specific OSSEC IDS manager                       | `POST`                                  |
| `/logs/host-manager?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`        | Get logs of a specific host manager                            | `POST`                                  |
| `/logs/ossec-ids?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`           | Get logs of a specific OSSEC IDS                               | `POST`                                  |
| `/logs/snort-ids?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`           | Get logs of a specific Snort IDS                               | `POST`                                  |
| `/logs/kafka?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`               | Get logs of a specific Kafka server                            | `POST`                                  |
| `/logs/elk-stack?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`           | Get logs of a specific ELK stack                               | `POST`                                  |
| `/logs/ryu-controller?token=<valid_token>&emulation=<emulation_name>&executionid=<execution_id>`      | Get logs of a specific Ryu controller                          | `POST`                                  |
| `/config?token=<valid_token>`                                                                         | Get/Update system configuration                                | `GET`,`PUT`                             |
| `/config/registration-allowed`                                                                        | Get registration policy                                        | `GET`                                   |
| `/version`                                                                                            | Get the version of CSLE management system                      | `GET`                                   |
| `/about-page`                                                                                         | Get the about page                                             | `GET`                                   |
| `/login-page`                                                                                         | Get the login page                                             | `GET`                                   |
| `/server-cluster-page`                                                                                | Get the server-cluster page                                    | `GET`                                   |
| `/register-page`                                                                                      | Get the register page                                          | `GET`                                   |
| `/emulation-statistics-page`                                                                          | Get the emulation-statistics                                   | `GET`                                   |
| `/emulations-page`                                                                                    | Get the emulation page                                         | `GET`                                   |
| `/images-page`                                                                                        | Get the images page                                            | `GET`                                   |
| `/downloads-page`                                                                                     | Get the downloads page                                         | `GET`                                   |
| `/jobs-page`                                                                                          | Get the jobs page                                              | `GET`                                   |
| `/monitoring-page`                                                                                    | Get the monitoring page                                        | `GET`                                   |
| `/policies-page`                                                                                      | Get the policies page                                          | `GET`                                   |
| `/policy-examination-page`                                                                            | Get the policy-examination page                                | `GET`                                   |
| `/sdn-controllers-page`                                                                               | Get the SDN-controllers page                                   | `GET`                                   |
| `/control-plane-page`                                                                                 | Get the control-plane page                                     | `GET`                                   |
| `/user-admin-page`                                                                                    | Get the user administration page                               | `GET`                                   |
| `/system-admin-page`                                                                                  | Get the system administration page                             | `GET`                                   |
| `/logs-admin-page`                                                                                    | Get the logs administration page                               | `GET`                                   |
| `/simulations-page`                                                                                   | Get the simulations page                                       | `GET`                                   |
| `/system-models-page`                                                                                 | Get the system models page                                     | `GET`                                   |
| `/traces-page`                                                                                        | Get the traces page                                            | `GET`                                   |
| `/training-page`                                                                                      | Get the training page                                          | `GET`                                   |
| `/container-terminal-page`                                                                            | Get the container-terminal page                                | `GET`                                   |
| `/server-cluster?token=<valid_token>`                                                                 | Get details of the server cluster                              | `GET`                                   |

## Requirements

- Python 3.8+
- `flask` (for HTTP server)
- `csle-base`
- `csle-common`
- `csle-agents`
- `csle-cluster`
- `csle-system-identification`
- `csle-ryu`
- `bcrypt` (for encrypting user credentials)
- `pyopenssl` (for encrypting user credentials)
- `eventlet` (for HTTP server)
- `dnspython` (for HTTP server)
- `gevent` (for HTTP server)
- `paramiko` (for terminal emulation)
- `types-paramiko` (for terminal emulation)
- `requests` (for making HTTP requests)
- `types-requests` (for making HTTP requests)

## Development Requirements

- Python 3.8+
- `flake8` (for linting)
- `flake8-rst-docstrings` (for linting docstrings)
- `tox` (for automated testing)
- `pytest` (for unit tests)
- `pytest-cov` (for unit test coverage)
- `mypy` (for static typing)
- `mypy-extensions` (for static typing)
- `mypy-protobuf` (for static typing)
- `types-PyYaml` (for static typing)
- `types-paramiko` (for static typing)
- `types-protobuf` (for static typing)
- `types-requests` (for static typing)
- `types-urllib3` (for static typing)
- `sphinx` (for API documentation)
- `sphinxcontrib-napoleon` (for API documentation)
- `sphinx-rtd-theme` (for API documentation)
- `pytest-mock` (for mocking tests)
- `pytest-grpc` (for grpc tests)

## Installation

```bash
# install from pip
pip install csle-rest-api==<version>
# local install from source
$ pip install -e csle-rest-api
# or (equivalently):
make install
# force upgrade deps
$ pip install -e csle-rest-api --upgrade
# git clone and install from source
git clone https://github.com/Limmen/csle
cd csle/simulation-system/libs/csle-rest-api
pip3 install -e .
# Install development dependencies
$ pip install -r requirements_dev.txt
```

### Development tools

Install all development tools at once:
```bash
make install_dev
```
or
```bash
pip install -r requirements_dev.txt
```
## API documentation

This section contains instructions for generating API documentation using `sphinx`.

### Latest Documentation

The latest documentation is available
at [https://limmen.dev/csle/docs/csle-rest-api](https://limmen.dev/csle/docs/csle-rest-api)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:

```bash
echo $CSLE_HOME
```

Then generate the documentation with the commands:

```bash
cd docs
sphinx-apidoc -f -o source/ ../csle_rest_api/
make html
```

To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle), copy the generated HTML
files to the documentation folder:

```bash
cp -r build/html ../../../../docs/_docs/csle-rest-api
```

To run all documentation commands at once, use the command:
```bash
make docs
```

## Static code analysis

To run the Python linter, execute the following command:
```
flake8 .
# or (equivalently):
make lint
```

To run the mypy type checker, execute the following command:
```
mypy .
# or (equivalently):
make types
```

## Unit tests

To run the unit tests, execute the following command:
```
pytest
# or (equivalently):
make unit_tests
```

To run tests of a specific test suite, execute the following command:
```
pytest -k "ClassName"
```

To generate a coverage report, execute the following command:
```
pytest --cov=csle_rest_api
```

## Run tests and code analysis in different python environments

To run tests and code analysis in different python environemnts, execute the following command:

```bash
tox
# or (equivalently):
make tests
```

## Create a new release and publish to PyPi

First build the package by executing:
```bash
python3 -m build
# or (equivalently)
make build
```
After running the command above, the built package is available at `./dist`.

Push the built package to PyPi by running:
```bash
python3 -m twine upload dist/*
# or (equivalently)
make push
```

To run all commands for the release at once, execute:
```bash
make release
```


## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020-2023, Kim Hammar

