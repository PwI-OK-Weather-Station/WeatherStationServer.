import json
from flask import request, send_from_directory
from flask.cli import FlaskGroup

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cli()

