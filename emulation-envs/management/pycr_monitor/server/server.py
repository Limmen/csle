from flask import Flask, jsonify
from gym_pycr_ctf.envs_model.config.generator.env_info import EnvInfo
from waitress import serve

app = Flask(__name__, static_url_path='', static_folder='../build/')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/envs')
def environments():
    envs = EnvInfo.parse_env_infos()
    envs_dicts = list(map(lambda x: x.to_dict(), envs))
    response = jsonify(envs_dicts)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=7777)
    #app.run(port=7777,host='0.0.0.0')
