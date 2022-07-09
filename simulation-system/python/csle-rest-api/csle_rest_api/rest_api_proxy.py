from flask import Flask
from requests import get

app = Flask(__name__)
SITE_NAME = 'http://172.31.212.92:7777/'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    print("path1")
    return get(f'{SITE_NAME}{path}').content

@app.route('/<path:path>/<path:path2>')
def proxy_1(path, path2):
    print("path2")
    return get(f'{SITE_NAME}{path}/{path2}').content

@app.route('/<path:path>/<path:path2>/<path:path3>')
def proxy_2(path, path2, path3):
    print("path3")
    return get(f'{SITE_NAME}{path}/{path2}/{path3}').content

@app.route('/<path:path>/<path:path2>/<path:path3>/<path:path4>')
def proxy_3(path, path2, path3, path4):
    print("path4")
    return get(f'{SITE_NAME}{path}/{path2}/{path3}/{path4}').content

@app.route('/<path:path>/<path:path2>/<path:path3>/<path:path4>/<path:path5>')
def proxy_4(path, path2, path3, path4, path5):
    print("path5")
    return get(f'{SITE_NAME}{path}/{path2}/{path3}/{path4}/{path5}').content

@app.route('/static/<path:path1>')
def static_1(path1):
    print("static")
    return get(f'{SITE_NAME}static/{path1}').content

@app.route('/static/<path:path1>/<path:path2>')
def static_2(path1, path2):
    print("static2")
    return get(f'{SITE_NAME}static/{path1}/{path2}').content

@app.route('/static/<path:path1>/<path:path2>/<path:path3>')
def static_3(path1, path2, path3):
    print("static3")
    return get(f'{SITE_NAME}static/{path1}/{path2}/{path3}').content

@app.route('/static/<path:path1>/<path:path2>/<path:path3>/<path:path4>')
def static_4(path1, path2, path3, path4):
    print("static4")
    return get(f'{SITE_NAME}static/{path1}/{path2}/{path3}/{path4}').content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)