from flask import Flask, url_for, jsonify
from flask import render_template
from flask import request
import socket
import json
PORT = 5000
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def create():
    result = json.dumps(request.form)
    print(result)
    #ligada = request.form.get('lampada')
    #ar = request.form.get('ar')
    s.send(result.encode('utf-8'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8080, debug=True)
