#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import redirect
from flask import abort
import logging
from logging.handlers import RotatingFileHandler
from mode import mode

app = Flask(__name__, static_url_path='')
control = mode()

@app.route('/')
def index():
    return render_template('index.html', animation_list=control.get_animation_list(), argument_list=control.get_argument_list(), mode_list=control.get_mode_list(), brightness=str(control.get_brightness()))

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/animation/<path:path>/')
def animation(path):
    control.animation_call(path)
    return redirect("/", code=302)

@app.route('/arg/<path:path>/')
def button(path):
    control.arg_call(path)
    return redirect("/", code=302)

@app.route('/modes/<path:path>/')
def mode(path):
    control.mode_call(path)
    return redirect("/", code=302)

@app.route('/brightness/<path:path>/', methods=['POST'])
def brightness(path):
    control.set_brightness(path)
    return ('', 204)
    
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
