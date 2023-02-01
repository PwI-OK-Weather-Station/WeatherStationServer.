import json
import flask
from flask import request, send_from_directory, jsonify
from flask.cli import FlaskGroup
from utility import authorize
import jwt
import os
import random
import string
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
from random import choice, randint
from server import app, db, User, Measurement, Device

cli = FlaskGroup(app)


def send_file(file):
    return send_from_directory('../client2/build', file)



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
            resp = flask.make_response({'token':token, 'name': user.name, 'uid': user.id})
            resp.set_cookie('token', token, samesite="Lax")
            resp.set_cookie('name', user.name, samesite="Lax")
            return resp, 200

    return {'Error':"Błędne dane logowania"}, 400
    
@app.get('/api/auth')
def auth():
    authStat = authorize(request)
    if authStat['id'] <= 0:
        return {'Error': "Brak autoryzacji"}, 400
    return {'Message': 'Authorized', 'id': authStat['id'], 'name': authStat['name']}, 200

@app.post('/api/logout')
def logout():
    resp = flask.make_response({'token': None, 'name': None})
    resp.set_cookie('token', '', expires=0)
    resp.set_cookie('name', '', expires=0)
    return resp, 200

@app.post('/api/device')
def addDevice():
    authStat = authorize(request)
    if authStat['id'] <= 0:
        return {'Error': "Brak autoryzacji"}, 400
    if 'content-type' in request.headers:
        if 'application/json' in request.headers['content-type']:
            if 'name' in request.json:
                dev = Device(**{
                    'token': ''.join(random.choice(string.ascii_lowercase+string.digits) for i in range(8)),
                    'name': request.json['name'], 
                    'users_id': authStat['id']
                    })
                if 'indoor' in request.json:
                    dev.indoor = request.json['indoor']
                if 'public' in request.json:
                    dev.public = request.json['public']

                db.session.add(dev)
                db.session.commit()
                return {"Success": "Poprawnie utworzono urządzenie"}, 200
    return {"Error": "Złe dane do kreacji urządzenia"}, 400

@app.get('/api/devices')
def list_devices():
    authStat = authorize(request)
    condition = ""
    conn = db.engine.connect()
    print(authStat['id'])
    if authStat['id'] <= 0:
        condition = f"WHERE d.public = TRUE" 
    elif authStat['admin']:
        condition = ""
    else:
        condition = f"WHERE d.public = TRUE or u.id = {authStat['id']}"
    query = query = f"SELECT d.id, d.name, u.id, u.name, d.public, d.indoor, d.location_latitude, d.location_longitude \
FROM devices d inner join users u on d.users_id = u.id {condition} ORDER BY d.id;"
    queryResult = conn.execute(query)
    result = []
    for row in queryResult:
        result.append({'device_id': row[0] ,'device_name':row[1], 'owner_id': row[2], 'owner_name': row[3], 'is_public': row[4],
        'indoor': row[5], 'location_latitude': row[6], 'location_longitude': row[7]})

    return {'devices':result},200

@app.get('/api/mindevices')
def list_mindevices():
    authStat = authorize(request)
    condition = ""
    conn = db.engine.connect()
    print(authStat['id'])
    if authStat['id'] <= 0:
        condition = f"WHERE d.public = TRUE" 
    elif authStat['admin']:
        condition = ""
    else:
        condition = f"WHERE d.public = TRUE or u.id = {authStat['id']}"
    query = query = f"SELECT d.id, d.name, u.id, u.name, d.public, d.indoor, d.location_latitude, d.location_longitude \
FROM devices d inner join users u on d.users_id = u.id {condition} ORDER BY d.id;"
    queryResult = conn.execute(query)
    result = []
    for row in queryResult:
        result.append({'id': row[0] ,'name':row[1]})

    return {'devices':result},200
    

@app.get('/api/device/<int:id>')
def device_info(id):
    device = Device.query.filter_by(id=id).first()
    if device:
        authStat = authorize(request)
        if authStat['id'] <= 0:
            measurements = Measurement.query.filter_by(devices_id=id).all()
        else:
            """"TO DO - lepsza filtracja tak aby uniemożliwić podglądanie przez innych użytkowników"""
            measurements = Measurement.query.filter_by(devices_id=id).all()
        result = []
        for row in measurements:
            result.append({'temperature': row.temperature ,'pressure':row.pressure, 'humidity':row.humidity, 'create_time':row.create_time})
        return {'id':device.id, 'name':device.name ,'measurements':result},200
    return {"Error": "Brak dostępu do pomiarów"}, 400

@app.get('/api/device/<int:id>/<int:count>')
def device_info_limited(id,count):
    device = Device.query.filter_by(id=id).first()
    if device:
        authStat = authorize(request)
        if authStat['id'] <= 0:
            measurements = Measurement.query.filter_by(devices_id=id).order_by(Measurement.create_time.desc()).limit(count)
        else:
            """"TO DO - lepsza filtracja tak aby uniemożliwić podglądanie przez innych użytkowników"""
            measurements = Measurement.query.filter_by(devices_id=id).order_by(Measurement.create_time.desc()).limit(count)
        result = []
        for row in measurements:
            result.append({'temperature': row.temperature ,'pressure':row.pressure, 'humidity':row.humidity, 'create_time':row.create_time})
        return {'id':device.id, 'name':device.name ,'measurements':result},200
    return {"Error": "Brak dostępu do pomiarów"}, 400

@app.get('/api/device/<int:id>/config')
def device_config(id):
    authStat = authorize(request)
    if authStat['id'] <= 0:
        return {'Error': "Brak autoryzacji"}, 400
    device = Device.query.filter_by(users_id=authStat['id'], id=id).first()
    if device:
        return {'id':device.id, 'public': device.public, 'indoor': device.indoor,
        'location_latitude': device.location_latitude, 'location_longitude': device.location_longitude,
        'name': device.name, 'token': device.token }, 200
    return {'Error': "Brak dostępu do urządzenia"}, 400

@app.post('/api/device/<string:token>')
def device_post_meassurement(token):
    device = Device.query.filter_by(token=token).first()
    if 'content-type' in request.headers:
        if 'application/json' in request.headers['content-type']:
            if device is not None:
                if 'pressure' not in request.json:
                    request.json['pressure'] = None
                if 'temperature' not in request.json:
                    request.json['temperature'] = None
                if 'humidity' not in request.json:
                    request.json['humidity'] = None
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

