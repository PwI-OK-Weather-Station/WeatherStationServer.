import click
import sqlalchemy
import random
import string
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import choice, randint
from  werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object('server.config.Config')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), unique=True, nullable=False)
    admin = db.Column(db.Boolean, unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    location_latitude = db.Column(db.Numeric(precision=9, scale=6))
    location_longitude = db.Column(db.Numeric(precision=9, scale=6))
    name = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), nullable=False, unique=True)
    users_id = db.Column(db.Integer, nullable=False)


class Measurement(db.Model):
    __tablename__='measurements'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Numeric(precision=9, scale=6))
    pressure = db.Column(db.Numeric(precision=9, scale=6))
    humidity = db.Column(db.Numeric(precision=9, scale=6))
    devices_id = db.Column(db.Integer, nullable=False)


def execute_sql_file(filename):
    engine = db.engine
    with engine.connect() as con:
        sql_file = open(f'server/{filename}.sql', 'r')
        escaped_sql = sqlalchemy.text(sql_file.read())
        con.execute(escaped_sql)


@app.cli.command('seeddb')
def seed_db():
    """Seeds database with testing questions by running `flask seeddb`"""
    execute_sql_file('seed')


@app.cli.command('createdb')
def create_db():
    """Creates database by running `flask createdb`"""
    execute_sql_file('schema')
    print()

@app.cli.command('createuser')
@click.argument('email')
@click.argument('password')
@click.argument('name')
def add_user(email, password, name):
    print("{} {} {}\n".format(email, password, name))
    user = User(**{'email':email,'password':generate_password_hash(password), 'name':name, 'admin':False})
    print(user)
    db.session.add(user)
    db.session.commit()
    print("user added")


@app.cli.command('createdevice')
@click.argument('name')
@click.argument('users_id')
def add_device(name, users_id):
    device = Device(**{'name':name, 'token': ''.join(random.choice(string.ascii_lowercase+string.digits) for i in range(8)),'users_id': users_id})
    db.session.add(device)
    db.session.commit()
    print("device added")
