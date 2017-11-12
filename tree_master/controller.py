#!/usr/bin/env python2

from animator import animator
from value_store import storage
from ledmaster import led_master
import sys

class controller(object):

    def __init__(self):
        self.s = storage('config.ini')
        self.led = led_master(ramp_up_speed=self._getint("ramp_up"), calm_down_speed=self._getint("calm_down"), retention=self._getint("retention"))
        self.led.start()
        self.ani = animator(self.led)
        self._change_mode(self._getstr("mode"))

        self.DEFAULT_RAMP_UP = 20
        self.DEFAULT_CALM_DOWN = 2
        self.DEFAULT_RETENTION = 10
        self.DEFAULT_MODE = "off"

        self.RAMP_UP_MIN = 1
        self.RAMP_UP_MAX = self.led.CONST_MAX_INTENSITY
        self.CALM_DOWN_MIN = 1
        self.CALM_DOWN_MAX = self.led.CONST_MAX_INTENSITY
        self.RETENTION_MIN = 1
        self.RETENTION_MAX = 1000

        self.MODE_LIST = [ ("off", "OFF"),
                      ("snake", "Snake"),
                      ("rand", "Random"),
                      ("snow", "Snow"),
                    ]

        self.PLUSMINUS_LIST = [ ("ramp_up", "Ramp up: "),
                           ("calm_down", "Calm down: "),
                           ("retention", "Retention: "),
                         ]

    def _getint(self, name):
        try:
            i = int(self.s.get_value(name))
            if i is None:
                if name == "ramp_up":
                    self.s.set_value("ramp_up", self.DEFAULT_RAMP_UP)
                elif name == "calm_down":
                    self.s.set_value("calm_down", self.DEFAULT_CALM_DOWN)
                elif name == "retention":
                    self.s.set_value("retention", self.DEFAULT_RETENTION)
            return i
        except ValueError:
            return None

    def _getstr(self, name):
        try:
            i = str(self.s.get_value(name))
            if i is None:
                if name == "mode":
                    self.s.set_value("mode", self.DEFAULT_MODE)
            return i
        except ValueError:
            return None

    def _change_mode(self, mode_name):
        self.ani.stop_animation()
        self.ani.set_animation(mode_name)
        self.ani.start_animation()

    def _change_attr(self, attr_name, attr_value):
        if attr_name == "ramp_up" and attr_value >= self.RAMP_UP_MIN and attr_value <= self.RAMP_UP_MAX:
            self.s.set_value(attr_name, attr_value)
            self.led.set_ramp_up_speed(attr_value)
        elif attr_name == "calm_down" and attr_value >= self.CALM_DOWN_MIN and attr_value <= self.CALM_DOWN_MAX:
            self.s.set_value(attr_name, attr_value)
            self.led.set_calm_down_speed(attr_value)
        elif attr_name == "retention" and attr_value >= self.RETENTION_MIN and attr_value <= self.RETENTION_MAX:
            self.s.set_value(attr_name, attr_value)
            self.led.set_retention(attr_value)

    def get_function_list(self):
        l = []
        for identifier, name in self.MODE_LIST:
            l.append(('button', name, 'Select', self.ani.get_animation_name() == identifier, "mode_"+identifier, None))
        for identifier, name in self.PLUSMINUS_LIST:
            l.append(('plusminus', name+self._getstr(identifier), None, None, "value_"+identifier+"_plus", "value_"+identifier+"_minus"))
        return l

    def api_call(self, call):
        for identifier, name in self.MODE_LIST:
            if "mode_"+identifier == call:
                self._change_mode(identifier)
                break
        for identifier, name in self.PLUSMINUS_LIST:
            if "value_"+identifier+"_plus" == call:
                self._change_attr(identifier, self._getint(identifier)+1)
                break
            elif "value_"+identifier+"_minus" == call:
                self._change_attr(identifier, self._getint(identifier)-1)
                break
