from flask import Flask, jsonify
from pycr_common.dao.network.trajectory import Trajectory
from waitress import serve

app = Flask(__name__, static_url_path='', static_folder='../build/')


@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/demo')
def demo():
    return app.send_static_file('index.html')

@app.route('/log')
def log():
    return app.send_static_file('index.html')

@app.route('/log/defender')
def log_defender():
    return app.send_static_file('index.html')

@app.route('/log/attacker')
def log_attacker():
    return app.send_static_file('index.html')

@app.route('/config')
def config():
    return app.send_static_file('index.html')

@app.route('/config/attacker')
def config_attacker():
    return app.send_static_file('index.html')

@app.route('/config/attacker/actionspace')
def config_attacker_actionspace():
    return app.send_static_file('index.html')

@app.route('/config/attacker/staticpolicy')
def config_attacker_staticpolicy():
    return app.send_static_file('index.html')

@app.route('/config/defender')
def config_defender():
    return app.send_static_file('index.html')

@app.route('/config/defender/actionspace')
def config_defender_actionspace():
    return app.send_static_file('index.html')

@app.route('/config/infrastructure/containers')
def config_infra_containers():
    return app.send_static_file('index.html')

@app.route('/config/infrastructure/vulnerabilities')
def config_infra_vulns():
    return app.send_static_file('index.html')

@app.route('/config/infrastructure/flags')
def config_infra_flags():
    return app.send_static_file('index.html')

@app.route('/config/infrastructure/firewalls')
def config_infra_firewalls():
    return app.send_static_file('index.html')

@app.route('/config/infrastructure/users')
def config_infra_users():
    return app.send_static_file('index.html')

@app.route('/config/infrastructure/clients')
def config_infra_clients():
    return app.send_static_file('index.html')

@app.route('/training')
def training():
    return app.send_static_file('index.html')

@app.route('/training/defender')
def training_defender():
    return app.send_static_file('index.html')

@app.route('/training/attacker')
def training_attacker():
    return app.send_static_file('index.html')

@app.route('/trajectories')
def trajectories():
    taus: dict = Trajectory.load_trajectories_json(
        trajectories_save_dir="./",
        trajectories_file="one_tau.json")
    response = jsonify(taus)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8888)
    #app.run(port=7777,host='0.0.0.0')


# New entries
#