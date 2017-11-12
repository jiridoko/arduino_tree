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

app = Flask(__name__, static_url_path='')

    #s = storage('test2.out')
    #print str(s.get_value("test"))
    #s.set_value("test", "val")
    #print str(s.get_value("test"))
    #s.set_value("test2", 56)
    #print str(int(s.get_value("test2"))+2)

global s
s = storage('config.ini')
if s.get_value("ramp_up") is None:
    s.set_value("ramp_up", 20)
if s.get_value("calm_down") is None:
    s.set_value("calm_down", 2)
if s.get_value("retention") is None:
    s.set_value("retention", 10)

led = led_master(ramp_up_speed=int(s.get_value("ramp_up")), calm_down_speed=int(s.get_value("calm_down")), retention=int(s.get_value("retention")))

ani = animator(led)
led.start()

global function_list
# elementType, nameL, nameR, highlighted, idPlus, idMinus
function_list = [ ('button', 'Off', 'Select', True, 1, None),
                  ('button', 'Snake', 'Select', False, 2, None),
                  ('button', 'Snowfall', 'Select', False, 3, None),
                  ('plusminus', 'Ramp up: '+s.get_value("ramp_up"), None, None, 4, 5),
                  ('plusminus', 'Calm down: '+s.get_value("calm_down"), None, None, 6, 7),
                  ('plusminus', 'Retention: '+s.get_value("retention"), None, None, 8, 9),
                  ]

def update_ramp_up(new_value):
    s.set_value("ramp_up", new_value)
    led.set_ramp_up_speed(new_value)
    global function_list
    elementType, nameL, nameR, highlighted, idPlus, idMinus = function_list[3]
    nameL = "Ramp up: "+str(new_value)
    function_list[3] = (elementType, nameL, nameR, highlighted, idPlus, idMinus)

def update_calm_down(new_value):
    s.set_value("calm_down", new_value)
    led.set_calm_down_speed(new_value)
    global function_list
    elementType, nameL, nameR, highlighted, idPlus, idMinus = function_list[4]
    nameL = "Calm down: "+str(new_value)
    function_list[4] = (elementType, nameL, nameR, highlighted, idPlus, idMinus)

def update_retention(new_value):
    s.set_value("retention", new_value)
    led.set_retention(new_value)
    global function_list
    elementType, nameL, nameR, highlighted, idPlus, idMinus = function_list[5]
    nameL = "Retention: "+str(new_value)
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
        ani.stop_animation()
        s.set_value("mode", "off")
    elif path == "2":
        update_highlight(0, False)
        update_highlight(1, True)
        update_highlight(2, False)
        ani.stop_animation()
        ani.set_animation("snake")
        ani.start_animation()
        s.set_value("mode", "snake")
    elif path == "3":
        update_highlight(0, False)
        update_highlight(1, False)
        update_highlight(2, True)
        ani.stop_animation()
        ani.set_animation("rand")
        ani.start_animation()
        s.set_value("mode", "snow")
    elif path == "4":
        update_ramp_up(int(s.get_value("ramp_up"))+1)
    elif path == "5":
        update_ramp_up(int(s.get_value("ramp_up"))-1)
    elif path == "6":
        update_calm_down(int(s.get_value("calm_down"))+1)
    elif path == "7":
        update_calm_down(int(s.get_value("calm_down"))-1)
    elif path == "8":
        update_retention(int(s.get_value("retention"))+1)
    elif path == "9":
        update_retention(int(s.get_value("retention"))-1)
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
        program = s.get_value("mode", default=None)
        if program == "off":
            update_highlight(0, True)
            update_highlight(1, False)
            update_highlight(2, False)
            ani.stop_animation()
        elif program == "snake":
            update_highlight(0, False)
            update_highlight(1, True)
            update_highlight(2, False)
            ani.stop_animation()
            ani.set_animation("snake")
            ani.start_animation()
        elif program == "snow":
            update_highlight(0, False)
            update_highlight(1, False)
            update_highlight(2, True)
            ani.stop_animation()
            ani.set_animation("rand")
            ani.start_animation()

        app.run(host="0.0.0.0", port=80)
    except KeyboardInterrupt:
        print "interrupt"
        ani.set_showing(False)
        ani.disable()
        led.set_updating(False)
