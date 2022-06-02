import base64
import time
import os
from flask import Flask, jsonify, request
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.container_manager import ContainerManager
from csle_common.util.read_emulation_statistics import ReadEmulationStatistics
from csle_common.controllers.emulation_env_manager import EmulationEnvManager
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
from csle_common.controllers.simulation_env_manager import SimulationEnvManager
from csle_common.util.emulation_util import EmulationUtil
from csle_agents.job_controllers.training_job_manager import TrainingJobManager
from csle_system_identification.job_controllers.data_collection_job_manager import DataCollectionJobManager
from csle_system_identification.job_controllers.system_identification_job_manager import SystemIdentificationJobManager
import json
from waitress import serve

app = Flask(__name__, static_url_path='', static_folder='../build/')


@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')

@app.route('/emulations', methods=['GET'])
def emulationspage():
    return app.send_static_file('index.html')

@app.route('/simulations', methods=['GET'])
def simulationspage():
    return app.send_static_file('index.html')

@app.route('/monitoring', methods=['GET'])
def monitoringpage():
    return app.send_static_file('index.html')

@app.route('/traces', methods=['GET'])
def tracespage():
    return app.send_static_file('index.html')

@app.route('/emulationstatistics', methods=['GET'])
def statisticspage():
    return app.send_static_file('index.html')

@app.route('/systemmodels', methods=['GET'])
def modelspage():
    return app.send_static_file('index.html')

@app.route('/policyexamination', methods=['GET'])
def policy_examination_page():
    return app.send_static_file('index.html')

@app.route('/images', methods=['GET'])
def images_page():
    return app.send_static_file('index.html')

@app.route('/training', methods=['GET'])
def training_page():
    return app.send_static_file('index.html')

@app.route('/policies', methods=['GET'])
def policies_page():
    return app.send_static_file('index.html')

@app.route('/jobs', methods=['GET'])
def jobs_page():
    return app.send_static_file('index.html')

@app.route('/about', methods=['GET'])
def about_page():
    return app.send_static_file('index.html')

@app.route('/nodeexporter', methods=['GET', 'POST'])
def node_exporter():
    running = MonitorToolsController.is_node_exporter_running()
    port = constants.COMMANDS.NODE_EXPORTER_PORT
    node_exporter_dict = {
        "running": running,
        "port": port,
        "url": f"http://localhost:{port}/"
    }
    response = jsonify(node_exporter_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/prometheus', methods=['GET', 'POST'])
def prometheus():
    running = MonitorToolsController.is_prometheus_running()
    port = constants.COMMANDS.PROMETHEUS_PORT
    if request.method == "POST":
        if running:
            MonitorToolsController.stop_prometheus()
            running = False
        else:
            MonitorToolsController.start_prometheus()
            running = True
    prometheus_dict = {
        "running": running,
        "port": port,
        "url": f"http://localhost:{port}/"
    }
    response = jsonify(prometheus_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/cadvisor', methods=['GET', 'POST'])
def cadvisor():
    running = MonitorToolsController.is_cadvisor_running()
    port = constants.COMMANDS.CADVISOR_PORT
    if request.method == "POST":
        if running:
            MonitorToolsController.stop_cadvisor()
            running = False
        else:
            MonitorToolsController.start_cadvisor()
            running = True
    cadvisor_dict = {
        "running": running,
        "port": port,
        "url": f"http://localhost:{port}/"
    }
    response = jsonify(cadvisor_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/grafana', methods=['GET', 'POST'])
def grafana():
    running = MonitorToolsController.is_grafana_running()
    port = constants.COMMANDS.GRAFANA_PORT
    if request.method == "POST":
        if running:
            MonitorToolsController.stop_grafana()
            running = False
        else:
            MonitorToolsController.start_grafana()
            running = True
    grafana_dict = {
        "running": running,
        "port": port,
        "url": f"http://localhost:{port}/"
    }
    response = jsonify(grafana_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/imagesdata', methods=['GET'])
def images():
    images=ContainerManager.list_all_images()
    images_dicts = []
    for img in images:
        images_dicts.append(
            {
                "name": img[0],
                "size": img[4]
            }
        )
    response = jsonify(images_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/simulationsdata', methods=['GET'])
def simulations():
    all_simulations = MetastoreFacade.list_simulations()
    all_images = MetastoreFacade.list_simulation_images()
    for sim in all_simulations:
        for sim_name_img in all_images:
            sim_name, img = sim_name_img
            if sim_name == sim.name:
                sim.image = base64.b64encode(img).decode()
    simulations_dicts = list(map(lambda x: x.to_dict(), all_simulations))
    response = jsonify(simulations_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/simulationsdataids', methods=['GET'])
def simulation_ids():
    simulation_ids = MetastoreFacade.list_simulation_ids()
    response_dicts = []
    for tup in simulation_ids:
        response_dicts.append({
            "id": tup[0],
            "simulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/simulationsdata/get/<simulation_id>', methods=['GET'])
def get_simulation(simulation_id: int):
    simulation = MetastoreFacade.get_simulation(simulation_id)
    if simulation is None:
        response = jsonify({})
    else:
        response = jsonify(simulation.to_dict())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/simulationsdata/remove/<simulation_name>', methods=['POST'])
def remove_simulation(simulation_name: str):
    all_simulations = MetastoreFacade.list_simulations()
    for simulation in all_simulations:
        if simulation.name == simulation_name:
            SimulationEnvManager.uninstall_simulation(simulation)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/simulationsdata/remove', methods=['POST'])
def remove_all_simulations():
    all_simulations = MetastoreFacade.list_simulations()
    for simulation in all_simulations:
        SimulationEnvManager.uninstall_simulation(simulation)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/emulationsdata', methods=['GET'])
def emulations():
    all_emulations = MetastoreFacade.list_emulations()
    all_images = MetastoreFacade.list_emulation_images()
    rc_emulations = ContainerManager.list_running_emulations()
    for em in all_emulations:
        if em.name in rc_emulations:
            em.running = True
        else:
            em.running = False
        for em_name_img in all_images:
            em_name, img = em_name_img
            if em_name == em.name:
                em.image = base64.b64encode(img).decode()
    emulations_dicts = list(map(lambda x: x.to_dict(), all_emulations))
    response = jsonify(emulations_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/emulationsdataids', methods=['GET'])
def emulationids():
    emulation_ids = MetastoreFacade.list_emulations_ids()
    response_dicts = []
    for tup in emulation_ids:
        response_dicts.append({
            "id": tup[0],
            "emulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/monitor/<emulation>/<minutes>', methods=['GET'])
def monitor_emulation(emulation: str, minutes: int):
    minutes = int(minutes)
    em = MetastoreFacade.get_emulation_by_name(name=emulation)
    if em is None:
        time_series = None
    else:
        time_series = ReadEmulationStatistics.read_all(emulation_env_config=em, time_window_minutes=minutes).to_dict()
    response = jsonify(time_series)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/emulationsdata/<emulation_name>', methods=['GET', 'POST'])
def emulation(emulation_name: str):
    em = MetastoreFacade.get_emulation_by_name(name=emulation_name)
    rc_emulations = ContainerManager.list_running_emulations()
    if em is not None:
        if em.name in rc_emulations:
            em.running = True
        if request.method == "POST":
            if em.running:
                EmulationEnvManager.stop_containers(emulation_env_config=em)
                EmulationEnvManager.rm_containers(emulation_env_config=em)
                try:
                    ContainerManager.stop_docker_stats_thread(log_sink_config=em.log_sink_config,
                                                              containers_config=em.containers_config,
                                                              emulation_name=em.name)
                except Exception as e:
                    pass
                EmulationEnvManager.delete_networks_of_emulation_env_config(emulation_env_config=em)
                em.running = False
            else:
                EmulationEnvManager.run_containers(emulation_env_config=em)
                EmulationEnvManager.apply_emulation_env_config(emulation_env_config=em)
                em.running = True
    if em is None:
        em_dict = {}
    else:
        em_name, img = MetastoreFacade.get_emulation_image(emulation_name=em.name)
        em.image = base64.b64encode(img).decode()
        em_dict = em.to_dict()
    response = jsonify(em_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/emulationsdata/get/<emulation_id>', methods=['GET'])
def emulation_by_id(emulation_id: int):
    em = MetastoreFacade.get_emulation(id=emulation_id)
    rc_emulations = ContainerManager.list_running_emulations()
    if em is not None:
        if em.name in rc_emulations:
            em.running = True
    if em is None:
        em_dict = {}
    else:
        em_name, img = MetastoreFacade.get_emulation_image(emulation_name=em.name)
        em.image = base64.b64encode(img).decode()
        em_dict = em.to_dict()
    response = jsonify(em_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/emulationsdata/remove/<emulation_name>', methods=['POST'])
def remove_emulation(emulation_name: str):
    emulations = MetastoreFacade.list_emulations()
    rc_emulations = ContainerManager.list_running_emulations()
    for emulation in emulations:
        if emulation.name == emulation_name:
            if emulation_name in rc_emulations:
                EmulationEnvManager.clean_emulation(emulation)
            EmulationEnvManager.uninstall_emulation(config=emulation)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/emulationsdata/remove', methods=['POST'])
def remove_all_emulation():
    emulations = MetastoreFacade.list_emulations()
    rc_emulations = ContainerManager.list_running_emulations()
    for emulation in emulations:
        if emulation.name in rc_emulations:
            EmulationEnvManager.clean_emulation(emulation)
        EmulationEnvManager.uninstall_emulation(config=emulation)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/emulationtracesids', methods=['GET'])
def emulation_traces_ids():
    ids_emulations = MetastoreFacade.list_emulation_traces_ids()
    response_dicts = []
    for tup in ids_emulations:
        response_dicts.append({
            "id": tup[0],
            "emulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/emulationtraces', methods=['GET'])
def emulation_traces():
    emulation_trcs = MetastoreFacade.list_emulation_traces()
    traces_dicts = list(map(lambda x: x.to_dict(), emulation_trcs))
    response = jsonify(traces_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/emulationtraces/get/<emulation_trace_id>', methods=['GET'])
def get_emulation_trace(emulation_trace_id: int):
    trace = MetastoreFacade.get_emulation_trace(id=emulation_trace_id)
    if trace is None:
        response = jsonify({})
    else:
        response = jsonify(trace.to_dict())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/emulationtraces/remove/<emulation_trace_id>', methods=['POST'])
def remove_emulation_trace(emulation_trace_id: int):
    trace = MetastoreFacade.get_emulation_trace(id=emulation_trace_id)
    if trace is not None:
        MetastoreFacade.remove_emulation_trace(trace)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/emulationtraces/remove', methods=['POST'])
def remove_all_emulation_traces():
    traces = MetastoreFacade.list_emulation_traces()
    for trace in traces:
        MetastoreFacade.remove_emulation_trace(trace)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/simulationtraces', methods=['GET'])
def simulation_traces():
    simulation_trcs = MetastoreFacade.list_simulation_traces()
    traces_dicts = list(map(lambda x: x.to_dict(), simulation_trcs))
    response = jsonify(traces_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/simulationtracesids', methods=['GET'])
def simulation_traces_ids():
    simulation_trcs_ids = MetastoreFacade.list_simulation_traces_ids()
    response_dicts = []
    for tup in simulation_trcs_ids:
        response_dicts.append({
            "id": tup[0],
            "simulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/simulationtraces/get/<simulation_trace_id>', methods=['GET'])
def get_simulation_trace(simulation_trace_id: int):
    trace = MetastoreFacade.get_simulation_trace(id=simulation_trace_id)
    if trace is None:
        response = jsonify({})
    else:
        response = jsonify(trace.to_dict())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/simulationtraces/remove/<simulation_trace_id>', methods=['POST'])
def remove_simulation_trace(simulation_trace_id: int):
    trace = MetastoreFacade.get_simulation_trace(id=simulation_trace_id)
    if trace is not None:
        MetastoreFacade.remove_simulation_trace(trace)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/simulationtraces/remove', methods=['POST'])
def remove_all_simulation_traces():
    traces = MetastoreFacade.list_simulation_traces()
    for trace in traces:
        MetastoreFacade.remove_simulation_trace(trace)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/emulationstatisticsdata', methods=['GET'])
def emulation_statistics():
    stats = MetastoreFacade.list_emulation_statistics()
    stats_dicts = list(map(lambda x: x.to_dict(), stats))
    response = jsonify(stats_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/emulationstatisticsdataids', methods=['GET'])
def emulation_statistics_ids():
    stats_ids = MetastoreFacade.list_emulation_statistics_ids()
    response_dicts = []
    for tup in stats_ids:
        response_dicts.append({
            "id": tup[0],
            "emulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/emulationstatisticsdata/get/<emulation_statistics_id>', methods=['GET'])
def get_emulation_statistic(emulation_statistics_id: int):
    statistic = MetastoreFacade.get_emulation_statistic(id=emulation_statistics_id)
    if statistic is not None:
        response = jsonify(statistic.to_dict())
    else:
        response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/emulationstatisticsdata/remove/<emulation_statistics_id>', methods=['POST'])
def remove_emulation_statistic(emulation_statistics_id: int):
    statistic = MetastoreFacade.get_emulation_statistic(id=emulation_statistics_id)
    if statistic is not None:
        MetastoreFacade.remove_emulation_statistic(statistic)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/systemmodelsdata', methods=['GET'])
def system_models_data():
    models = MetastoreFacade.list_gaussian_mixture_system_models()
    models_dicts = list(map(lambda x: x.to_dict(), models))
    response = jsonify(models_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/systemmodelsdataids', methods=['GET'])
def system_models_ids():
    models_ids = MetastoreFacade.list_gaussian_mixture_system_models_ids()
    response_dicts = []
    for tup in models_ids:
        response_dicts.append({
            "id": tup[0],
            "emulation": tup[1],
            "statistic_id": tup[2]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/systemmodelsdata/remove/<system_model_id>', methods=['POST'])
def remove_system_model(system_model_id: int):
    model = MetastoreFacade.get_gaussian_mixture_system_model_config(id=system_model_id)
    if model is not None:
        MetastoreFacade.remove_gaussian_mixture_system_model(gaussian_mixture_system_model=model)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/systemmodelsdata/get/<system_model_id>', methods=['GET'])
def get_system_model(system_model_id: int):
    model = MetastoreFacade.get_gaussian_mixture_system_model_config(id=system_model_id)
    if model is not None:
        response = jsonify(model.to_dict())
    else:
        response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/experimentsdata', methods=['GET'])
def experiments():
    experiments = MetastoreFacade.list_experiment_executions()
    experiment_dicts = list(map(lambda x: x.to_dict(), experiments))
    response = jsonify(experiment_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/experimentsdataids', methods=['GET'])
def experiments_ids():
    experiments_ids = MetastoreFacade.list_experiment_executions_ids()
    response_dicts = []
    for tup in experiments_ids:
        response_dicts.append({
            "id": tup[0],
            "simulation": tup[1],
            "emulation": tup[2]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/experimentsdata/get/<experiment_id>', methods=['GET'])
def get_experiment(experiment_id: int):
    experiment = MetastoreFacade.get_experiment_execution(id=experiment_id)
    if experiment is not None:
        response = jsonify(experiment.to_dict())
    else:
        response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/experimentsdata/remove/<experiment_id>', methods=['POST'])
def remove_experiment(experiment_id: int):
    experiment = MetastoreFacade.get_experiment_execution(id=experiment_id)
    if experiment is not None:
        MetastoreFacade.remove_experiment_execution(experiment_execution=experiment)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/experimentsdata/remove', methods=['POST'])
def remove_all_experiments():
    experiments = MetastoreFacade.list_experiment_executions()
    for exp in experiments:
        MetastoreFacade.remove_experiment_execution(experiment_execution=exp)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/multithresholdpolicies', methods=['GET'])
def policies():
    multi_threshold_stopping_policies = MetastoreFacade.list_multi_threshold_stopping_policies()
    multi_threshold_stopping_policies_dicts = list(map(lambda x: x.to_dict(), multi_threshold_stopping_policies))
    response = jsonify(multi_threshold_stopping_policies_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/multithresholdpoliciesids', methods=['GET'])
def multi_threshold_policies_ids():
    multi_threshold_stopping_policies_ids = MetastoreFacade.list_multi_threshold_stopping_policies_ids()
    response_dicts = []
    for tup in multi_threshold_stopping_policies_ids:
        response_dicts.append({
            "id": tup[0],
            "simulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/multithresholdpolicies/get/<multi_threshold_stopping_policy_id>', methods=['GET'])
def get_multi_threshold_policy(multi_threshold_stopping_policy_id: int):
    policy = MetastoreFacade.get_multi_threshold_stopping_policy(id=multi_threshold_stopping_policy_id)
    if policy is not None:
        response = jsonify(policy.to_dict())
    else:
        response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/multithresholdpolicies/remove/<multi_threshold_stopping_policy_id>', methods=['POST'])
def remove_multi_threshold_policy(multi_threshold_stopping_policy_id: int):
    policy = MetastoreFacade.get_multi_threshold_stopping_policy(id=multi_threshold_stopping_policy_id)
    if policy is not None:
        MetastoreFacade.remove_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/multithresholdpolicies/remove', methods=['POST'])
def remove_all_multi_threshold_policies():
    policies = MetastoreFacade.list_multi_threshold_stopping_policies()
    for policy in policies:
        MetastoreFacade.remove_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/ppopolicies', methods=['GET'])
def ppo_policies():
    ppo_policies = MetastoreFacade.list_ppo_policies()
    ppo_policies_dicts = list(map(lambda x: x.to_dict(), ppo_policies))
    response = jsonify(ppo_policies_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/ppopoliciesids', methods=['GET'])
def ppo_policies_ids():
    ppo_policies_ids = MetastoreFacade.list_ppo_policies_ids()
    response_dicts = []
    for tup in ppo_policies_ids:
        response_dicts.append({
            "id": tup[0],
            "simulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/ppopolicies/get/<ppo_policy_id>', methods=['GET'])
def get_ppo_policy(ppo_policy_id: int):
    policy = MetastoreFacade.get_ppo_policy(id=ppo_policy_id)
    if policy is not None:
        response = jsonify(policy.to_dict())
    else:
        response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/ppopolicies/remove/<ppo_policy_id>', methods=['POST'])
def remove_ppo_policy(ppo_policy_id: int):
    policy = MetastoreFacade.get_ppo_policy(id=ppo_policy_id)
    if policy is not None:
        MetastoreFacade.remove_ppo_policy(ppo_policy=policy)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/ppopolicies/remove', methods=['POST'])
def remove_all_ppo_policies():
    policies = MetastoreFacade.list_ppo_policies()
    for policy in policies:
        MetastoreFacade.remove_ppo_policy(ppo_policy=policy)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/dqnpolicies', methods=['GET'])
def dqn_policies():
    dqn_policies = MetastoreFacade.list_dqn_policies()
    dqn_policies_dicts = list(map(lambda x: x.to_dict(), dqn_policies))
    response = jsonify(dqn_policies_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/dqnpoliciesids', methods=['GET'])
def dqn_policies_ids():
    dqn_policies_ids = MetastoreFacade.list_dqn_policies_ids()
    response_dicts = []
    for tup in dqn_policies_ids:
        response_dicts.append({
            "id": tup[0],
            "simulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/dqnpolicies/get/<dqn_policy_id>', methods=['GET'])
def get_dqn_policy(dqn_policy_id: int):
    policy = MetastoreFacade.get_dqn_policy(id=dqn_policy_id)
    if policy is not None:
        response = jsonify(policy.to_dict())
    else:
        response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/dqnpolicies/remove/<dqn_policy_id>', methods=['POST'])
def remove_dqn_policy(dqn_policy_id: int):
    policy = MetastoreFacade.get_dqn_policy(id=dqn_policy_id)
    if policy is not None:
        MetastoreFacade.remove_dqn_policy(dqn_policy=policy)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/dqnpolicies/remove', methods=['POST'])
def remove_all_dqn_policies():
    policies = MetastoreFacade.list_dqn_policies()
    for policy in policies:
        MetastoreFacade.remove_dqn_policy(dqn_policy=policy)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/tabularpolicies', methods=['GET'])
def tabular_policies():
    tabular_policies = MetastoreFacade.list_tabular_policies()
    tabular_policies_dicts = list(map(lambda x: x.to_dict(), tabular_policies))
    response = jsonify(tabular_policies_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/tabularpoliciesids', methods=['GET'])
def tabular_policies_ids():
    tabular_policies_ids = MetastoreFacade.list_tabular_policies_ids()
    response_dicts = []
    for tup in tabular_policies_ids:
        response_dicts.append({
            "id": tup[0],
            "simulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/tabularpolicies/get/<tabular_policy_id>', methods=['GET'])
def get_tabular_policy(tabular_policy_id: int):
    policy = MetastoreFacade.get_tabular_policy(id=tabular_policy_id)
    if policy is not None:
        response = jsonify(policy.to_dict())
    else:
        response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/tabularpolicies/remove/<tabular_policy_id>', methods=['POST'])
def remove_tabular_policy(tabular_policy_id: int):
    policy = MetastoreFacade.get_tabular_policy(id=tabular_policy_id)
    if policy is not None:
        MetastoreFacade.remove_tabular_policy(tabular_policy=policy)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/tabularpolicies/remove', methods=['POST'])
def remove_all_tabular_policies():
    policies = MetastoreFacade.list_tabular_policies()
    for policy in policies:
        MetastoreFacade.remove_tabular_policy(tabular_policy=policy)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/alphavecpolicies', methods=['GET'])
def alpha_vec_policies():
    alpha_vec_policies = MetastoreFacade.list_alpha_vec_policies()
    alpha_vec_policies_dicts = list(map(lambda x: x.to_dict(), alpha_vec_policies))
    response = jsonify(alpha_vec_policies_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/alphavecpoliciesids', methods=['GET'])
def alpha_vec_policies_ids():
    alpha_vec_policies_ids = MetastoreFacade.list_alpha_vec_policies_ids()
    response_dicts = []
    for tup in alpha_vec_policies_ids:
        response_dicts.append({
            "id": tup[0],
            "simulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/alphavecpolicies/get/<alpha_vec_policy_id>', methods=['GET'])
def get_alpha_vec_policy(alpha_vec_policy_id: int):
    policy = MetastoreFacade.get_alpha_vec_policy(id=alpha_vec_policy_id)
    if policy is not None:
        response = jsonify(policy.to_dict())
    else:
        response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/alphavecpolicies/remove/<alpha_vec_policy_id>', methods=['POST'])
def remove_alpha_vec_policy(alpha_vec_policy_id: int):
    policy = MetastoreFacade.get_alpha_vec_policy(id=alpha_vec_policy_id)
    if policy is not None:
        MetastoreFacade.remove_alpha_vec_policy(alpha_vec_policy=policy)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/alphavecpolicies/remove', methods=['POST'])
def remove_all_alpha_vec_policies():
    policies = MetastoreFacade.list_alpha_vec_policies()
    for policy in policies:
        MetastoreFacade.remove_alpha_vec_policy(alpha_vec_policy=policy)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/trainingjobs', methods=['GET'])
def trainingjobs():
    training_jobs = MetastoreFacade.list_training_jobs()
    alive_jobs = []
    for job in training_jobs:
        if EmulationUtil.check_pid(job.pid):
            job.running = True
        alive_jobs.append(job)
    training_jobs_dicts = list(map(lambda x: x.to_dict(), alive_jobs))
    response = jsonify(training_jobs_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/trainingjobsids', methods=['GET'])
def trainingjobsids():
    training_jobs_ids = MetastoreFacade.list_training_jobs_ids()
    response_dicts = []
    for tup in training_jobs_ids:
        response_dicts.append({
            "id": tup[0],
            "simulation": tup[1],
            "emulation": tup[2]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/trainingjobs/get/<job_id>', methods=['GET'])
def get_trainingjob(job_id: int):
    job = MetastoreFacade.get_training_job_config(id=job_id)
    if job is not None:
        if EmulationUtil.check_pid(job.pid):
            job.running = True
        response = jsonify(job.to_dict())
    else:
        response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/trainingjobs/stop/<job_id>', methods=['POST'])
def stop_trainingjob(job_id: int):
    job = MetastoreFacade.get_training_job_config(id=job_id)
    if job is not None:
        MonitorToolsController.stop_pid(pid=job.pid)
        time.sleep(2)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/trainingjobs/start/<job_id>', methods=['POST'])
def start_trainingjob(job_id: int):
    job = MetastoreFacade.get_training_job_config(id=job_id)
    if job is not None:
        TrainingJobManager.start_training_job_in_background(training_job=job)
        time.sleep(2)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/trainingjobs/remove/<job_id>', methods=['POST'])
def remove_trainingjob(job_id: int):
    job = MetastoreFacade.get_training_job_config(id=job_id)
    if job is not None:
        MonitorToolsController.stop_pid(job.pid)
        MetastoreFacade.remove_training_job(training_job=job)
        time.sleep(2)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/trainingjobs/remove', methods=['POST'])
def remove_all_trainingjobs():
    jobs = MetastoreFacade.list_training_jobs()
    for job in jobs:
        MonitorToolsController.stop_pid(job.pid)
        MetastoreFacade.remove_training_job(training_job=job)
    time.sleep(2)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/datacollectionjobs', methods=['GET'])
def datacollectionjobs():
    data_collection_jobs = MetastoreFacade.list_data_collection_jobs()
    alive_jobs = []
    for job in data_collection_jobs:
        if EmulationUtil.check_pid(job.pid):
            job.running = True
        alive_jobs.append(job)
    data_collection_jobs_dicts = list(map(lambda x: x.to_dict(), alive_jobs))
    response = jsonify(data_collection_jobs_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/datacollectionjobsids', methods=['GET'])
def datacollectionjobsids():
    data_collection_jobs_ids = MetastoreFacade.list_data_collection_jobs_ids()
    response_dicts = []
    for tup in data_collection_jobs_ids:
        response_dicts.append({
            "id": tup[0],
            "emulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/datacollectionjobs/get/<job_id>', methods=['GET'])
def get_data_collection_job(job_id: int):
    job = MetastoreFacade.get_data_collection_job_config(id=job_id)
    if job is not None:
        if EmulationUtil.check_pid(job.pid):
            job.running = True
        response = jsonify(job.to_dict())
    else:
        response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/datacollectionjobs/stop/<job_id>', methods=['POST'])
def stop_data_collection_job(job_id: int):
    job = MetastoreFacade.get_data_collection_job_config(id=job_id)
    if job is not None:
        MonitorToolsController.stop_pid(job.pid)
        time.sleep(2)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/datacollectionjobs/remove/<job_id>', methods=['POST'])
def remove_data_collection_job(job_id: int):
    job = MetastoreFacade.get_data_collection_job_config(id=job_id)
    if job is not None:
        MonitorToolsController.stop_pid(job.pid)
        MetastoreFacade.remove_data_collection_job(data_collection_job=job)
        time.sleep(2)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/datacollectionjobs/remove', methods=['POST'])
def remove_all_data_collection_jobs():
    jobs = MetastoreFacade.list_data_collection_jobs()
    for job in jobs:
        MonitorToolsController.stop_pid(job.pid)
        MetastoreFacade.remove_data_collection_job(data_collection_job=job)
    time.sleep(2)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/datacollectionjobs/start/<job_id>', methods=['POST'])
def start_data_collection_job(job_id: int):
    job = MetastoreFacade.get_data_collection_job_config(id=job_id)
    if job is not None:
        DataCollectionJobManager.start_data_collection_job_in_background(data_collection_job=job)
        time.sleep(4)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/systemidentificationjobs', methods=['GET'])
def system_identification_jobs():
    system_identification_jbos = MetastoreFacade.list_system_identification_jobs()
    alive_jobs = []
    for job in system_identification_jbos:
        if EmulationUtil.check_pid(job.pid):
            job.running = True
        alive_jobs.append(job)
    system_identification_jobs_dicts = list(map(lambda x: x.to_dict(), alive_jobs))
    response = jsonify(system_identification_jobs_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/systemidentificationjobsids', methods=['GET'])
def system_identification_jobs_ids():
    system_identification_jobs_ids = MetastoreFacade.list_system_identification_jobs_ids()
    response_dicts = []
    for tup in system_identification_jobs_ids:
        response_dicts.append({
            "id": tup[0],
            "emulation": tup[1]
        })
    response = jsonify(response_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/systemidentificationjobs/get/<job_id>', methods=['GET'])
def get_system_identification_job(job_id: int):
    job = MetastoreFacade.get_system_identification_job_config(id=job_id)
    if job is not None:
        if EmulationUtil.check_pid(job.pid):
            job.running = True
        response = jsonify(job.to_dict())
    else:
        response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/systemidentificationjobs/stop/<job_id>', methods=['POST'])
def stop_system_identification_job(job_id: int):
    job = MetastoreFacade.get_system_identification_job_config(id=job_id)
    if job is not None:
        MonitorToolsController.stop_pid(job.pid)
        time.sleep(2)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/systemidentificationjobs/remove/<job_id>', methods=['POST'])
def remove_system_identification_job(job_id: int):
    job = MetastoreFacade.get_system_identification_job_config(id=job_id)
    if job is not None:
        MonitorToolsController.stop_pid(job.pid)
        MetastoreFacade.remove_system_identification_job(system_identification_job=job)
        time.sleep(2)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/systemidentificationjobs/remove', methods=['POST'])
def remove_all_system_identification_jobs():
    jobs = MetastoreFacade.list_system_identification_jobs()
    for job in jobs:
        MonitorToolsController.stop_pid(job.pid)
        MetastoreFacade.remove_system_identification_job(system_identification_job=job)
    time.sleep(2)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/systemidentificationjobs/start/<job_id>', methods=['POST'])
def start_system_identification_job(job_id: int):
    job = MetastoreFacade.get_system_identification_job_config(id=job_id)
    if job is not None:
        SystemIdentificationJobManager.start_system_identification_job_in_background(system_identification_job=job)
        time.sleep(4)
    response = jsonify({})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/emulationsimulationtraces', methods=['GET'])
def emulationsimulationtraces():
    # emulation_simulation_traces = MetastoreFacade.list_emulation_simulation_traces()
    # emulation_simulation_traces_dicts = list(map(lambda x: x.to_dict(), emulation_simulation_traces))
    # response = jsonify(emulation_simulation_traces_dicts)
    f = open('/var/log/csle/one_tau.json')
    d = json.load(f)
    response = jsonify(d["trajectories"])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/file', methods=['POST'])
def read_file():
    path = json.loads(request.data)["path"]
    data = ""
    if os.path.exists(path):
        with open(path, 'r') as fp:
            data = fp.read()
    data_dict = {"logs": data}
    response = jsonify(data_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=7777, threads=100)
    #app.run(port=7777,host='0.0.0.0')
