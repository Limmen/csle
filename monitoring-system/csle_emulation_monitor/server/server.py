import base64
from flask import Flask, jsonify, request
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.container_manager import ContainerManager
from csle_common.util.read_emulation_statistics import ReadEmulationStatistics
from csle_common.controllers.emulation_env_manager import EmulationEnvManager
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from waitress import serve

app = Flask(__name__, static_url_path='', static_folder='../build/')


@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')


@app.route('/envs', methods=['GET'])
def environments():
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
    envs_dicts = list(map(lambda x: x.to_dict(), all_emulations))
    response = jsonify(envs_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/monitor/<envname>/<minutes>', methods=['GET'])
def monitor_env(envname: str, minutes: int):
    minutes = int(minutes)
    print(minutes)
    em = MetastoreFacade.get_emulation(name=envname)
    if em is None:
        time_series = None
    else:
        time_series = ReadEmulationStatistics.read_all(emulation_env_config=em, time_window_minutes=minutes).to_dict()
    response = jsonify(time_series)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/envs/<envname>', methods=['GET', 'POST'])
def env(envname: str):
    em = MetastoreFacade.get_emulation(name=envname)
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
                print("Running")
                EmulationEnvManager.run_containers(emulation_env_config=em)
                print("Config")
                EmulationEnvManager.apply_emulation_env_config(emulation_env_config=em)
                em.running = True
    if em is None:
        em_dict = {}
    else:
        em_name, img = MetastoreFacade.get_emulation_img(emulation_name=em.name)
        em.image = base64.b64encode(img).decode()
        em_dict = em.to_dict()
    response = jsonify(em_dict)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/emulation-traces', methods=['GET'])
def emulation_traces():
    emulation_trcs = MetastoreFacade.list_emulation_traces()
    traces_dicts = list(map(lambda x: x.to_dict(), emulation_trcs))
    response = jsonify(traces_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/simulation-traces', methods=['GET'])
def simulation_traces():
    simulation_trcs = MetastoreFacade.list_emulation_traces()
    traces_dicts = list(map(lambda x: x.to_dict(), simulation_trcs))
    response = jsonify(traces_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=7777)
    #app.run(port=7777,host='0.0.0.0')
