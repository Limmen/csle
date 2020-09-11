from flask import Flask, request, send_from_directory
from waitress import serve

app = Flask(__name__, static_url_path='', static_folder='/web/static')

@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(port=80,host='0.0.0.0')
#serve(app, host='0.0.0.0', port=80)