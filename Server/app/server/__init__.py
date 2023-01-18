import click
import sqlalchemy
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


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    location_latitude = db.Column(db.Numeric(precision=9, scale=6))
    location_longitude = db.Column(db.Numeric(precision=9, scale=6))
    name = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), nullable=False, unique=True)
    users_id = db.Column(db.Integer, nullable=False)


class Measurement(db.Model):
    __tablename= 'measurements'
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
    user = User({'email':email,'password':password, 'name':name})
    db.session.add(user)
    db.session.commit()
    print("user added\n")
    
