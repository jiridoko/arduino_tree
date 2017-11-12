#!/usr/bin/env python2
from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import redirect
import sys
import logging
from threading import Thread
from time import sleep
from ledmaster import led_master
from logging.handlers import RotatingFileHandler
from value_store import storage
from animator import animator
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

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=80)
