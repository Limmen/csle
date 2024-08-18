---
title: Web Interface 
permalink: /docs/web-interface/
---

## Web Interface

The web interface of CSLE can be used to view management information and to request management operations (see Fig. 17).****
It can also be used to monitor emulations in real-time
(see Fig. 18 and Fig. 19), to start or stop services (see Fig. 20), to monitor reinforcement learning workloads (see
Fig. 21), to access terminals of emulated components (see Fig. 22), and to examine security policies (see Fig. 23).

<p align="center">
<img src="./../../img/management_dropdown.png" width="75%">
<p class="captionFig">
Figure 17: The web interface of CSLE; 
this interface shows management information and and can be used to request management operations.
</p>
</p>

<p align="center">
<img src="./../../img/monitoring_page.png" width="75%">
<p class="captionFig">
Figure 18: The monitoring page of the web interface; 
this page allows a user to view system metrics of a given emulation execution in real-time.
</p>
</p>

<p align="center">
<img src="./../../img/statistics_page.png" width="75%">
<p class="captionFig">
Figure 19: The statistics page of the web interface; this page allows a user to view empirical statistics 
of emulated infrastructures, e.g., empirical distributions of system metrics.
</p>
</p>

<p align="center">
<img src="./../../img/control_plane_page_2.png" width="75%">
<p class="captionFig">
Figure 20: The control plane of the web interface; this page allows a user to 
request management operations, e.g., starting and stopping emulated components or services.
</p>
</p>

<p align="center">
<img src="./../../img/training_results.png" width="75%">
<p class="captionFig">
Figure 21 The training results page of the web interface; 
this page allows a user to view the results of reinforcement learning experiments.
</p>
</p>

<p align="center">
<img src="./../../img/container_terminal_page.png" width="75%">
<p class="captionFig">
Figure 22: The container-terminal page of the web interface; 
this page allows a user to execute arbitrary bash commands inside a container of an emulated infrastructure.
</p>
</p>

### The Policy Examination System

The policy examination system allows a user to traverse episodes of Markov decision processes in a controlled manner and
to track the actions triggered by security policies. Similar to a software debugger, a user can continue or or halt an
episode at any time-step and inspect parameters and probability distributions of interest. The system enables insight
into the structure of a given policy and in the behavior of a policy in edge cases. It is integrated with the rest of
the web interface and can be accessed as a regular web page (see Fig. 23).

<p align="center">
<img src="./../../img/policy_examination_page.png" width="75%">
<p class="captionFig">
Figure 23: The demonstration view of the policy examination system; 
the system allows a user to interactively step through an episode of a Markov decision process.
</p>
</p>

Figure 23 pictures the main user interface of the policy examination system. The left part of the interface shows the
defender's view and the right part shows the attacker's view. The plot on the upper left shows the defender's belief
about the infrastructure's state and the probability that the defender takes an action at each time-step. The plot on
the lower left shows the distribution of infrastructure metrics that the defender observes. The graphic on the right
shows the attacker's view, depicted as an overlay on the IT-infrastructure's topology.

The policy examination system provides insight into the structure of the defender policy and its behavior in edge-cases.
It can be used to observe correlations among the attacker's actions, the infrastructure metrics, and the actions that
the defender policy prescribes. It can also be used to examine which actions of the attacker are difficult for the
defender to detect or trigger actions by the defender.

### Implementation

The web interface is implemented by a web application written in JavaScript and the React framework, which executes on
the management system. Each physical server of the management system runs a Flask web server that exposes an HTTP REST
API
(the REST API is detailed in the subsequent section). In front of these web servers is a Nginx reverse proxy that load
balances client requests, decrypts incoming HTTPS traffic, and encrypts outgoing HTTP traffic using TLS
(see Fig. 24).

<p align="center">
<img src="./../../img/web_app_arch.png" width="60%">
<p class="captionFig">
Figure 24: Architecture diagram of the CSLE web application; 
a Nginx reverse proxy load balances requests to a group of Flask web servers, 
which expose HTTP REST APIs; these APIs can be used to view management information 
and to request management operations.
</p>
</p>

The web-based terminal emulation shown in Fig. 22 is implemented as follows. To create a web-based terminal session, the
web client's browser first opens a websocket to one of the HTTP servers. The server then opens an SSH tunnel to the
emulated device and creates a terminal session. This tunnel is then used to pipe commands and terminal responses between
the client and the terminal (see Fig. 25).

<p align="center">
<img src="./../../img/web_terminal.png" width="55%">
<p class="captionFig">
Figure 25: Architecture diagram of the web-based terminal emulation in CSLE; 
the web application in the client's browser opens a web socket to an HTTP server 
running on one of the physical servers of the management system; 
the web server then pipes the websocket to an SSH tunnel 
that connects to a terminal of the emulated component.
</p>
</p>

### The REST API

The endpoints of the REST API are listed in Tables 20-23. An example HTTP request and response is given below.

```bash
curl https://csle.dev/emulations?ids=true\&token=<my_token>
[{"emulation":"csle-level1-010","id":1,"running":false`,
{"emulation":"csle-level2-010","id":2,"running":false`,
{"emulation":"csle-level3-010","id":3,"running":false`,
{"emulation":"csle-level4-010","id":4,"running":false`,
{"emulation":"csle-level5-010","id":5,"running":false`,
{"emulation":"csle-level6-010","id":6,"running":false`,
{"emulation":"csle-level7-010","id":7,"running":false`,
{"emulation":"csle-level8-010","id":8,"running":false`,
{"emulation":"csle-level9-010","id":9,"running":true`,
{"emulation":"csle-level10-010","id":10,"running":false`,
{"emulation":"csle-level11-010","id":11,"running":false`,
{"emulation":"csle-level12-010","id":12,"running":false`]
```

<p class="captionFig">
Listing 3: An HTTP request for the `emulations` resource of the CSLE REST API (line 1) 
and the corresponding HTTP response (lines 2-13); 
the request includes the flag `ids=true`, 
which means that the response only includes the identifiers, names, and statuses of the emulations, 
rather than the full configurations; the request is performed with `curl`.
</p>

| *Resource*                                                             | *Method*                |
|------------------------------------------------------------------------|-------------------------|
| `/emulations`                                                          | `GET`, `DELETE`         |
| `/emulations?ids=true&token=<token>`                                   | `GET`, `DELETE`         |
| `/emulations/<em_id>?token=<token>`                                    | `GET`, `DELETE`, `POST` |
| `/emulations/<em_id>/executions?token=<token>`                         | `GET`, `DELETE`         |
| `/emulations/<em_id>/executions/<exec_id>?token=<token>`               | `GET`, `DELETE`         |
| `/emulations/<em_id>/executions/<exec_id>/monitor/<min>?token=<token>` | `GET`                   |
| `/simulations?token=<token>`                                           | `GET`, `DELETE`         |
| `/simulations?ids=true&token=<token>`                                  | `GET`, `DELETE`         |
| `/simulations/<simulation_id>?token=<token>`                           | `GET`, `DELETE`         |
| `/cadvisor?token=<token>`                                              | `POST`                  |
| `/nodeexporter?token=<token>`                                          | `POST`                  |
| `/grafana?token=<token>`                                               | `POST`                  |
| `/prometheus?token=<token>`                                            | `POST`                  |
| `/alpha-vec-policies?token=<token>`                                    | `GET`, `DELETE`         |
| `/alpha-vec-policies?ids=true&token=<token>`                           | `GET`, `DELETE`         |
| `/alpha-vec-policies/<policy_id>?token=<token>`                        | `GET`, `DELETE`         |
| `/dqn-policies?token=<token>`                                          | `GET`, `DELETE`         |
| `/dqn-policies?ids=true&token=<token>`                                 | `GET`, `DELETE`         |
| `/dqn-policies/<policy_id>?token=<token>`                              | `GET`, `DELETE`         |
| `/ppo-policies?token=<token>`                                          | `GET`, `DELETE`         |
| `/ppo-policies?ids=true&token=<token>`                                 | `GET`, `DELETE`         |
| `/ppo-policies/<policy_id>?token=<token>`                              | `GET`, `DELETE`         |
| `/vector-policies?token=<token>`                                       | `GET`, `DELETE`         |
| `/vector-policies?ids=true&token=<token>`                              | `GET`, `DELETE`         |
| `/vector-policies/<policy_id>?token=<token>`                           | `GET`, `DELETE`         |
| `/tabular-policies?token=<token>`                                      | `GET`, `DELETE`         |
| `/tabular-policies?ids=true&token=<token>`                             | `GET`, `DELETE`         |
| `/tabular-policies/<policy_id>?token=<token>`                          | `GET`, `DELETE`         |
| `/multi-threshold-policies?token=<token>`                              | `GET`, `DELETE`         |
| `/multi-threshold-policies?ids=true&token=<token>`                     | `GET`, `DELETE`         |
| `/multi-threshold-policies/<policy_id>?token=<token>`                  | `GET`, `DELETE`         |
| `/fnn-w-softmax-policies?token=<token>`                                | `GET`, `DELETE`         |
| `/fnn-w-softmax-policies?ids=true&token=<token>`                       | `GET`, `DELETE`         |
| `/fnn-w-softmax-policies/<policy_id>?token=<token>`                    | `GET`, `DELETE`         |
| `/training-jobs?token=<token>`                                         | `GET`, `DELETE`         |
| `/training-jobs?ids=true&token=<token>`                                | `GET`, `DELETE`         |
| `/training-jobs/<job_id>?token=<token>`                                | `GET`, `DELETE`, `POST` |
| `/data-collection-jobs?token=<token>`                                  | `GET`, `DELETE`         |
| `/data-collection-jobs?ids=true&token=<token>`                         | `GET`, `DELETE`         |
| `/data-collection-jobs/<job_id>?token=<token>`                         | `GET`, `DELETE`, `POST` |
| `/system-identification-jobs?token=<token>`                            | `GET`, `DELETE`         |
| `/system-identification-jobs?ids=true&token=<token>`                   | `GET`, `DELETE`         |
| `/system-identification-jobs/<job_id>?token=<token>`                   | `GET`, `DELETE`         |

<p class="captionFig">
Table 20: REST API resources (1/4).
</p>

| *Resource*                                                          | *Method*        |
|---------------------------------------------------------------------|-----------------|
| `/emulation-traces?token=<token>`                                   | `GET`, `DELETE` |
| `/emulation-traces?ids=true&token=<token>`                          | `GET`, `DELETE` |
| `/emulation-traces/<trace_id>?token=<token>`                        | `GET`, `DELETE` |
| `/simulation-traces?token=<token>`                                  | `GET`, `DELETE` |
| `/simulation-traces?ids=true&token=<token>`                         | `GET`, `DELETE` |
| `/simulation-traces/<trace_id>?token=<token>`                       | `GET`, `DELETE` |
| `/emulation-simulation-traces?token=<token>`                        | `GET`, `DELETE` |
| `/emulation-simulation-traces?ids=true&token=<token>`               | `GET`, `DELETE` |
| `/emulation-simulation-traces/<trace_id>?token=<token>`             | `GET`, `DELETE` |
| `/images?token=<token>`                                             | `GET`           |
| `/file?token=<token>`                                               | `POST`          |
| `/experiments?token=<token>`                                        | `GET`, `DELETE` |
| `/experiments?ids=true&token=<token>`                               | `GET`, `DELETE` |
| `/experiments/<trace_id>?token=<token>`                             | `GET`, `DELETE` |
| `/sdn-controllers?token=<token>`                                    | `GET`, `DELETE` |
| `/sdn-controllers?ids=true&token=<token>`                           | `GET`, `DELETE` |
| `/emulation-statistics?token=<token>`                               | `GET`, `DELETE` |
| `/emulation-statistics?ids=true&token=<token>`                      | `GET`, `DELETE` |
| `/emulation-statistics/<trace_id>?token=<token>`                    | `GET`, `DELETE` |
| `/gaussian-mixture-system-models?token=<token>`                     | `GET`, `DELETE` |
| `/gaussian-mixture-system-models?ids=true&token=<token>`            | `GET`, `DELETE` |
| `/gaussian-mixture-system-models/<trace_id>?token=<token>`          | `GET`, `DELETE` |
| `/empirical-system-models?token=<token>`                            | `GET`, `DELETE` |
| `/empirical-system-models?ids=true&token=<token>`                   | `GET`, `DELETE` |
| `/empirical-system-models/<trace_id>?token=<token>`                 | `GET`, `DELETE` |
| `/mcmc-system-models?token=<token>`                                 | `GET`, `DELETE` |
| `/mcmc-system-models?ids=true&token=<token>`                        | `GET`, `DELETE` |
| `/mcmc-system-models/<trace_id>?token=<token>`                      | `GET`, `DELETE` |
| `/gp-system-models?token=<token>`                                   | `GET`, `DELETE` |
| `/gp-system-models?ids=true&token=<token>`                          | `GET`, `DELETE` |
| `/gp-system-models/<model_id>?token=<token>`                        | `GET`, `DELETE` |
| `/system-models?ids=true&token=<token>`                             | `GET`           |
| `/login`                                                            | `POST`          |
| `/traces-datasets?token=<token>`                                    | `GET`, `DELETE` |
| `/traces-datasets?ids=true&token=<token>`                           | `GET`, `DELETE` |
| `/traces-datasets/<traces_datasets_id>?token=<token>`               | `GET`, `DELETE` |
| `/traces-datasets/<traces_datasets_id>?token=<token>&download=true` | `GET`           |
| `/server-cluster?token=<token>`                                     | `GET`           |
| `/pgadmin?token=<token>`                                            | `GET`, `POST`   |
| `/postgresql?token=<token>`                                         | `GET`, `POST`   |
| `/docker?token=<token>`                                             | `GET`, `POST`   |
| `/nginx?token=<token>`                                              | `GET`, `POST`   |
| `/flask?token=<token>`                                              | `GET`, `POST`   |
| `/clusterstatuses?token=<token>`                                    | `GET`           |
| `/logs/nginx?token=<token>`                                         | `POST`          |
| `/logs/postgresql?token=<token>`                                    | `POST`          |
| `/logs/docker?token=<token>`                                        | `POST`          |
| `/logs/flask?token=<token>`                                         | `POST`          |
| `/logs/clustermanager?token=<token>`                                | `POST`          |

<p class="captionFig">
Table 21: REST API resources (2/4).
</p>

| *Resource*                                                                          | *Method*               |
|-------------------------------------------------------------------------------------|------------------------|
| `/statistics-datasets?token=<token>`                                                | `GET`, `DELETE`        |
| `/statistics-datasets?ids=true&token=<token>`                                       | `GET`, `DELETE`        |
| `/statistics-datasets/<statistics_datasets_id>?token=<token>`                       | `GET`, `DELETE`        |
| `/statistics-datasets/<statistics_datasets_id>?token=<token>&download=true`         | `GET`                  |
| `/emulation-executions?token=<token>`                                               | `GET`, `DELETE`        |
| `/emulation-executions?ids=tru&token=<token>`                                       | `GET`, `DELETE`        |
| `/emulation-executions/<exec_id>?token=<token>`                                     | `GET`, `DELETE`        |
| `/emulation-executions/<exec_id>/info?token=<token>&emulation=<em>`                 | `GET`                  |
| `/emulation-executions/<exec_id>/docker-stats-manager?token=<token>&emulation=<em>` | `POST`                 |
| `/emulation-executions/<exec_id>/docker-stats-monitor?token=<token>&emulation=<em>` | `POST`                 |
| `/emulation-executions/<exec_id>/client-manager?token=<token>&emulation=<em>`       | `POST`                 |
| `/emulation-executions/<exec_id>/client-population?token=<token>&emulation=<em>`    | `POST`                 |
| `/emulation-executions/<exec_id>/client-producer?token=<token>&emulation=<em>`      | `POST`                 |
| `/emulation-executions/<exec_id>/kafka-manager?token=<token>&emulation=<em>`        | `POST`                 |
| `/emulation-executions/<exec_id>/kafka?token=<token>&emulation=<em>`                | `POST`                 |
| `/emulation-executions/<exec_id>/snort-ids-manager?token=<token>&emulation=<em>`    | `POST`                 |
| `/emulation-executions/<exec_id>/snort-ids-monitor?token=<token>&emulation=<em>`    | `POST`                 |
| `/emulation-executions/<exec_id>/snort-ids?token=<token>&emulation=<em>`            | `POST`                 |
| `/emulation-executions/<exec_id>/ossec-ids-manager?token=<token>&emulation=<em>`    | `POST`                 |
| `/emulation-executions/<exec_id>/ossec-ids?token=<token>&emulation=<em>`            | `POST`                 |
| `/emulation-executions/<exec_id>/ossec-ids-monitor?token=<token>&emulation=<em>`    | `POST`                 |
| `/emulation-executions/<exec_id>/host-manager?token=<token>&emulation=<em>`         | `POST`                 |
| `/emulation-executions/<exec_id>/host-monitor?token=<token>&emulation=<em>`         | `POST`                 |
| `/emulation-executions/<exec_id>/elk-manager?token=<token>&emulation=<em>`          | `POST`                 |
| `/emulation-executions/<exec_id>/elastic?token=<token>&emulation=<em>`              | `POST`                 |
| `/emulation-executions/<exec_id>/logstash?token=<token>&emulation=<em>`             | `POST`                 |
| `/emulation-executions/<exec_id>/kibana?token=<token>&emulation=<em>`               | `POST`                 |
| `/emulation-executions/<exec_id>/container?token=<token>&emulation=<em>`            | `POST`                 |
| `/emulation-executions/<exec_id>/elk-stack?token=<token>&emulation=<em>`            | `POST`                 |
| `/emulation-executions/<exec_id>/traffic-generator?token=<token>&emulation=<em>`    | `POST`                 |
| `/emulation-executions/<exec_id>/filebeat?token=<token>&emulation=<em>`             | `POST`                 |
| `/emulation-executions/<exec_id>/packetbeat?token=<token>&emulation=<em>`           | `POST`                 |
| `/emulation-executions/<exec_id>/metricbeat?token=<token>&emulation=<em>`           | `POST`                 |
| `/emulation-executions/<exec_id>/ryu-manager?token=<token>&emulation=<em>`          | `POST`                 |
| `/emulation-executions/<exec_id>/ryu-monitor?token=<token>&emulation=<em>`          | `POST`                 |
| `/emulation-executions/<exec_id>/ryu-controller?token=<token>&emulation=<em>`       | `POST`                 |
| `/emulation-executions/<exec_id>/switches?token=<token>&emulation=<em>`             | `POST`                 |
| `/users?token=<token>`                                                              | `GET`, `DELETE`, `PUT` |
| `/users?ids=true&token=<token>`                                                     | `GET`, `DELETE`        |
| `/users/<user_id>?token=<token>`                                                    | `GET`, `DELETE`, `PUT` |
| `/users/create`                                                                     | `POST`                 |
| `/logs?token=<token>`                                                               | `GET`                  |
| `/logs/docker-stats-manager?token=<token>`                                          | `GET`                  |
| `/logs/prometheus?token=<token>`                                                    | `GET`                  |


<p class="captionFig">
Table 22: REST API resources (3/4).
</p>

| *Resource*                                                                   | *Method*     |
|------------------------------------------------------------------------------|--------------|
| `/logs/grafana?token=<token>`                                                | `GET`        |
| `/logs/cadvisor?token=<token>`                                               | `GET`        |
| `/logs/container?token=<token>`                                              | `GET`        |
| `/logs/node-exporter?token=<token>`                                          | `GET`        |
| `/logs/client-manager?token=<token>&emulation=<em>&executionid=<exec_id>`    | `POST`       |
| `/logs/kafka-manager?token=<token>&emulation=<em>&executionid=<exec_id>`     | `POST`       |
| `/logs/elk-manager?token=<token>&emulation=<em>&executionid=<exec_id>`       | `POST`       |
| `/logs/ryu-manager?token=<token>&emulation=<em>&executionid=<exec_id>`       | `POST`       |
| `/logs/traffic-manager?token=<token>&emulation=<em>&executionid=<exec_id>`   | `POST`       |
| `/logs/snort-ids-manager?token=<token>&emulation=<em>&executionid=<exec_id>` | `POST`       |
| `/logs/ossec-ids-manager?token=<token>&emulation=<em>&executionid=<exec_id>` | `POST`       |
| `/logs/host-manager?token=<token>&emulation=<em>&executionid=<exec_id>`      | `POST`       |
| `/logs/ossec-ids?token=<token>&emulation=<em>&executionid=<exec_id>`         | `POST`       |
| `/logs/snort-ids?token=<token>&emulation=<em>&executionid=<exec_id>`         | `POST`       |
| `/logs/kafka?token=<token>&emulation=<em>&executionid=<exec_id>`             | `POST`       |
| `/logs/elk-stack?token=<token>&emulation=<em>&executionid=<exec_id>`         | `POST`       |
| `/logs/ryu-controller?token=<token>&emulation=<em>&executionid=<exec_id>`    | `POST`       |
| `/config?token=<token>`                                                      | `GET`, `PUT` |
| `/config/registration-allowed`                                               | `GET`        |
| `/version`                                                                   | `GET`        |
| `/about-page`                                                                | `GET`        |
| `/login-page`                                                                | `GET`        |
| `/register-page`                                                             | `GET`        |
| `/emulation-statistics-page`                                                 | `GET`        |
| `/emulations-page`                                                           | `GET`        |
| `/images-page`                                                               | `GET`        |
| `/downloads-page`                                                            | `GET`        |
| `/jobs-page`                                                                 | `GET`        |
| `/monitoring-page`                                                           | `GET`        |
| `/policies-page`                                                             | `GET`        |
| `/policy-examination-page`                                                   | `GET`        |
| `/sdn-controllers-page`                                                      | `GET`        |
| `/control-plane-page`                                                        | `GET`        |
| `/user-admin-page`                                                           | `GET`        |
| `/system-admin-page`                                                         | `GET`        |
| `/logs-admin-page`                                                           | `GET`        |
| `/simulations-page`                                                          | `GET`        |
| `/system-models-page`                                                        | `GET`        |
| `/traces-page`                                                               | `GET`        |
| `/training-page`                                                             | `GET`        |
| `/create-emulation-page`                                                     | `GET`        |
| `/container-terminal-page`                                                   | `GET`        |
| `/container-terminal?token=<token>`                                          | `Websockets` |
| `/create-emulation`                                                          | `POST`       |


<p class="captionFig">
Table 23: REST API resources (4/4).
</p>