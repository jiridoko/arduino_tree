#!/usr/bin/env python2

from animator import animator
from value_store import storage
from ledmaster import led_master
import sys

class controller(object):

    def __init__(self):
        self.s = storage('config.ini')
        self.led = led_master()
        self.led.start()
        self.ani = animator(self.led, self.s)
        self._change_mode(self._getstr("mode"))

        self.DEFAULT_MODE = "off"

        self.MODE_LIST = [ ("off", "OFF"),
                      ("snake", "Snake"),
                      ("rand", "Random"),
                      ("snow", "Snow"),
                    ]

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
        self.s.set_value("mode", mode_name)

    def get_function_list(self):
        l = []
        for identifier, name in self.MODE_LIST:
            l.append(('button', name, 'Select', self.ani.get_animation_name() == identifier, "mode_"+identifier, None))
        for identifier, name in self.ani.get_animation().get_argument_list():
            l.append(('plusminus', name+self.ani.get_animation().get_argument(identifier), None, None, "value_"+identifier+"_plus", "value_"+identifier+"_minus"))
        return l

    def api_call(self, call):
        for identifier, name in self.MODE_LIST:
            if "mode_"+identifier == call:
                self._change_mode(identifier)
                break
        for identifier, name in self.ani.get_animation().get_argument_list():
            if "value_"+identifier+"_plus" == call:
                self.ani.get_animation().set_argument(identifier, int(self.ani.get_animation().get_argument(identifier))+1)
                break
            elif "value_"+identifier+"_minus" == call:
                self.ani.get_animation().set_argument(identifier, int(self.ani.get_animation().get_argument(identifier))-1)
                break
