import click
import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import choice, randint

app = Flask(__name__)
app.config.from_object('server.config.Config')
db = SQLAlchemy(app)



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

