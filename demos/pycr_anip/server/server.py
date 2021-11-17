from flask import Flask, jsonify
from pycr_common.dao.network.trajectory import Trajectory
from waitress import serve

app = Flask(__name__, static_url_path='', static_folder='../build/')

@app.route('/')
def root():
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