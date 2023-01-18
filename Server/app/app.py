import json
from flask import request, send_from_directory, jsonify
from flask.cli import FlaskGroup
import jwt
import os
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
from server import app, db

cli = FlaskGroup(app)


def send_file(file):
    return send_from_directory('../client/public', file)



@app.route('/<path:path>')
def static_file(path):
    return send_file(path)


@app.route('/')
def root():
    return send_file('index.html')


@app.post('/login')
def login():
    token = jwt.encode({
               'login':request.json['login'], 
               'exp' : datetime.utcnow() + timedelta(minutes = 30)},
           app.config['SECRET_KEY']);
    return {'token':token}, 200
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cli()

