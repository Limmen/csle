from flask import Flask, jsonify
from csle_common.envs_model.config.generator.env_info import EnvInfo
from csle_common.envs_model.config.generator.metastore_facade import MetastoreFacade
from csle_common.envs_model.config.generator.container_manager import ContainerManager
from waitress import serve

app = Flask(__name__, static_url_path='', static_folder='../build/')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/envs')
def environments():
    envs = EnvInfo.parse_runnning_emulation_infos()
    envs_dicts = list(map(lambda x: x.to_dict(), envs))
    response = jsonify(envs_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/stopped_envs')
def stopped_environments():
    all_emulations = MetastoreFacade.list_emulations()
    rc_emulations = ContainerManager.list_running_emulations()
    stopped_emulations = []
    running_emulations = []
    for em in all_emulations:
        if em.name in rc_emulations:
            running_emulations.append(em)
        else:
            stopped_emulations.append(em)
    emulation_dicts = list(map(lambda x: x.to_dict(), stopped_emulations))
    response = jsonify(emulation_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=7777)
    #app.run(port=7777,host='0.0.0.0')
