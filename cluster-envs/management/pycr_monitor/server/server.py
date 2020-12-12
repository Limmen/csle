from flask import Flask, request, send_from_directory, jsonify
from waitress import serve

app = Flask(__name__, static_url_path='', static_folder='/web/static')

@app.route('/environments')
def environments():
    envs = {}
    envs["test"] = [1,2,3]
    response = jsonify(envs)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(port=7777,host='0.0.0.0')
#serve(app, host='0.0.0.0', port=80)