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

app = Flask(__name__, static_url_path='')

global ramp_up
global calm_down
global retention
ramp_up = 20
calm_down = 2
retention = 10

led = led_master(ramp_up_speed=ramp_up, calm_down_speed=calm_down, retention=retention)

class animator(Thread):
    def __init__(self, led):
        super(animator, self).__init__()
        self.led = led
        self.enabled = True
        self.showing = False
    def disable(self):
        self.enabled = False
    def set_showing(self, value):
        self.showing = value
        print "showing "+str(value)
    def run(self):
        while self.enabled:
            if self.showing:
                for i in xrange(0,80):
                    led.set_led_value(i, led.CONST_MAX_INTENSITY)
                    sleep(0.05)
                    if not self.showing:
                        break
            else:
                sleep(0.1)

ani = animator(led)
ani.start()
led.start()

global function_list
# elementType, nameL, nameR, highlighted, idPlus, idMinus
function_list = [ ('button', 'Off', 'Select', True, 1, None),
                  ('button', 'Snake', 'Select', False, 2, None),
                  ('button', 'Snowfall', 'Select', False, 3, None),
                  ('plusminus', 'Ramp up: 20', None, None, 4, 5),
                  ('plusminus', 'Calm down: 2', None, None, 6, 7),
                  ('plusminus', 'Retention: 10', None, None, 8, 9),
                  ]

def update_ramp_up(new_value):
    global ramp_up
    ramp_up = new_value
    led.set_ramp_up_speed(new_value)
    global function_list
    elementType, nameL, nameR, highlighted, idPlus, idMinus = function_list[3]
    nameL = "Ramp up: "+str(ramp_up)
    function_list[3] = (elementType, nameL, nameR, highlighted, idPlus, idMinus)

def update_calm_down(new_value):
    global calm_down
    calm_down = new_value
    led.set_calm_down_speed(new_value)
    global function_list
    elementType, nameL, nameR, highlighted, idPlus, idMinus = function_list[4]
    nameL = "Calm down: "+str(calm_down)
    function_list[4] = (elementType, nameL, nameR, highlighted, idPlus, idMinus)

def update_retention(new_value):
    global retention
    retention = new_value
    led.set_retention(new_value)
    global function_list
    elementType, nameL, nameR, highlighted, idPlus, idMinus = function_list[5]
    nameL = "Retention: "+str(retention)
    function_list[5] = (elementType, nameL, nameR, highlighted, idPlus, idMinus)

def update_highlight(index, set_to):
    global function_list
    elementType, nameL, nameR, highlighted, idPlus, idMinus = function_list[index]
    highlighted = set_to
    function_list[index] = (elementType, nameL, nameR, highlighted, idPlus, idMinus)

@app.route('/')
def hello():
    global function_list
    return render_template('index.html', function_list=function_list)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/<path:path>/')
def button(path):
    global function_list
    if path == "1":
        update_highlight(0, True)
        update_highlight(1, False)
        update_highlight(2, False)
        ani.set_showing(False)
    elif path == "2":
        update_highlight(0, False)
        update_highlight(1, True)
        update_highlight(2, False)
        ani.set_showing(True)
    elif path == "3":
        update_highlight(0, False)
        update_highlight(1, False)
        update_highlight(2, True)
        ani.set_showing(False)
    elif path == "4":
        update_ramp_up(ramp_up+1)
    elif path == "5":
        update_ramp_up(ramp_up-1)
    elif path == "6":
        update_calm_down(calm_down+1)
    elif path == "7":
        update_calm_down(calm_down-1)
    elif path == "8":
        update_retention(retention+1)
    elif path == "9":
        update_retention(retention-1)
    else:
        update_highlight(0, False);
        update_highlight(1, False);
        update_highlight(2, False);
    app.logger.info('Button pressed')
    return redirect("/", code=302)

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    try:
        app.run(host="0.0.0.0", port=80)
    except KeyboardInterrupt:
        print "interrupt"
        ani.set_showing(False)
        ani.disable()
        led.set_updating(False)
