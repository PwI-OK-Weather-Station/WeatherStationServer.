import json
from flask import request, send_from_directory, jsonify
from flask.cli import FlaskGroup
import jwt
import os
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
from server import app, db, User, Measurement, Device

cli = FlaskGroup(app)


def send_file(file):
    return send_from_directory('../client/public', file)



@app.route('/<path:path>')
def static_file(path):
    return send_file(path)


@app.route('/')
def root():
    return send_file('index.html')


@app.post('/api/login')
def login():
    if 'email' and 'password' in request.json:
        user = User.query.filter_by(email=request.json['email']).first()
        if user is not None and check_password_hash(user.password, request.json['password']):
            token = jwt.encode({
                    'id':user.id, 'name':user.name, 
                    'exp' : datetime.utcnow() + timedelta(minutes = 30)},
                app.config['SECRET_KEY']);
            return {'token':token, 'name': user.name}, 200

    return {'Error':"Błędne dane logowania"}, 400

@app.get('/api/devices')
def list_devices():
    devices = Device.query.all()
    result = []
    for row in devices:
        result.append({'id': row.id ,'name':row.name, 'owner':row.users_id})

    return {'devices':result},200
    

@app.get('/api/device/<int:id>')
def device_info(id):
    device = Device.query.filter_by(id=id).first()
    measurements = Measurement.query.filter_by(devices_id=id).all()
    result = []
    for row in measurements:
        result.append({'temperature': row.temperature ,'pressure':row.pressure, 'humidity':row.humidity})

    return {'id':device.id, 'name':device.name ,'measurements':result},200


@app.post('/api/device/<string:token>')
def device_post_meassurement(token):
    device = Device.query.filter_by(token=token).first()
    if device is not None:
        meas = Measurement(**{'temperature': request.json['temperature'], 
        'pressure': request.json['pressure'], 
        'humidity': request.json['humidity'],
        'devices_id': device.id})
        db.session.add(meas)
        db.session.commit()
        return {'message': "Success"}, 200
    return {'message':"Error"}, 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cli()

