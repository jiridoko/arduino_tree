#!/usr/bin/env python2
from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import redirect
from flask import abort
import logging
from logging.handlers import RotatingFileHandler
from controller import controller

app = Flask(__name__, static_url_path='')
control = controller()

@app.route('/')
def index():
    return render_template('index.html', function_list=control.get_function_list())

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/<path:path>/')
def button(path):
    control.api_call(path)
    return redirect("/", code=302)
    
@app.route('/direct/<path:path>/')
def direct(path):
    if control.direct_call(path):
        return ('', 204)
    else:
        return abort(404)

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    handler = RotatingFileHandler('controller.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=80)
