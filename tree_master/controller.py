#!/usr/bin/env python3

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
        self._change_animation(self._getstr("animation"))

        self.DEFAULT_ANIMATION = "off"

        self.ANIMATION_LIST = [ ("off", "OFF"),
                      ("snake", "Snake"),
                      ("rand", "Random"),
                      ("snow", "Snow"),
                      ("direct", "Direct"),
                    ]

    def _getstr(self, name):
        try:
            i = str(self.s.get_value(name))
            if i is None:
                if name == "animation":
                    self.s.set_value("animation", self.DEFAULT_ANIMATION)
            return i
        except ValueError:
            return None

    def _change_animation(self, animation_name):
        animation = animation_name
        if animation_name == "None":
            animation = "off"
        self.ani.stop_animation()
        self.ani.set_animation(animation)
        self.ani.start_animation()
        self.s.set_value("animation", animation)

    def get_function_list(self):
        l = []
        for identifier, name in self.ANIMATION_LIST:
            l.append(('button', name, 'Select', self.ani.get_animation_name() == identifier, "animation_"+identifier, None))
        for identifier, name in self.ani.get_animation().get_argument_list():
            l.append(('plusminus', name+self.ani.get_animation().get_argument(identifier), None, None, "value_"+identifier+"_plus", "value_"+identifier+"_minus"))
        return l

    def api_call(self, call):
        for identifier, name in self.ANIMATION_LIST:
            if "animation_"+identifier == call:
                self._change_animation(identifier)
                break
        for identifier, name in self.ani.get_animation().get_argument_list():
            if "value_"+identifier+"_plus" == call:
                self.ani.get_animation().set_argument(identifier, int(self.ani.get_animation().get_argument(identifier))+1)
                break
            elif "value_"+identifier+"_minus" == call:
                self.ani.get_animation().set_argument(identifier, int(self.ani.get_animation().get_argument(identifier))-1)
                break

    def direct_call(self, data):
        if self.ani.get_animation().get_name() == "direct":
            self.ani.get_animation().direct_call(data)
            return True
        else:
            return False
