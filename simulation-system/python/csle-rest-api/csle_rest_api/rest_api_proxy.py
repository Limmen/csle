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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)