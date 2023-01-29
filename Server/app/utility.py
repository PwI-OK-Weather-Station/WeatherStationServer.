import jwt
from server import app, db, User, Measurement, Device
def authorize(req):
    id = 0
    name = ""
    if 'token' in req.cookies:
        try:
            x = jwt.decode(req.cookies['token'], app.config['SECRET_KEY'], algorithms=['HS256'])
            id=x['id']
            name = x['name']
        except Exception as e:
            id = 0
    if 'content-type' in req.headers and id <= 0:
        if 'application/json' in req.headers['content-type']:
            if 'token' in req.json:
                try:
                    x = jwt.decode(req.json['token'], app.config['SECRET_KEY'], algorithms=['HS256'])
                    id = x['id']
                    name = x['name']
                except Exception as e:
                    id = 0
    if id > 0:
        user = User.query.filter_by(id=id, name=name).first()
        return {"id": user.id, "name": user.name, "email": user.email, "admin": user.admin}

    return {"id": id, "admin": False}