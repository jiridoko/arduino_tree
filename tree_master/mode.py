#!/usr/bin/env python3

from animator import animator
from value_store import storage
from ledmaster import led_master
import sys

class mode(object):

    def __init__(self):
        self.led = led_master()
        self.led.start()
        self.ani = animator(self.led)
        self.s = storage('config.ini')

        self.DEFAULT_ANIMATION = "off"

        self.ANIMATION_LIST = [ ("red_green", "Red&Green"),
                      ("rand", "Random"),
                      ("snow", "Snow"),
                      ("rainbow", "Rainbow"),
                    ]

        self.MODE_COUNT = 4
        self.current_mode = int(self.s.get_value("mode", default=-1))
        self.change_mode(self.current_mode)
        self.led.set_brightness(int(self.s.get_value("brightness", default=30)))

    def _getstr(self, name):
        try:
            i = str(self.s.get_value(name))
            if i is None:
                if name == "animation":
                    self.s.set_value("animation", self.DEFAULT_ANIMATION)
            return i
        except ValueError:
            return None

    def _change_animation(self, animation_name, store=True):
        animation = animation_name
        if animation_name == "None" or animation_name is None:
            animation = "off"
        self.ani.stop_animation()
        self.ani.set_animation(animation)
        for arg in self.ani.get_animation().get_argument_names():
            arg_value = self.s.get_value(arg, section=str(self.current_mode))
            if arg_value is not None:
                self.ani.get_animation().set_argument(arg, arg_value)
        self.ani.start_animation()
        if store:
            self.s.set_value("animation", animation, section=str(self.current_mode))

    def change_animation(self, animation_name):
        if self.current_mode >=0 and animation_name in [ident for ident, name in self.ANIMATION_LIST]:
            self._change_animation(animation_name)

    def get_mode_list(self):
			# {% for mode_name, mode_id, active in mode_list %}
        ret = [('-1', 'Off', 1 if self.current_mode == -1 else 0)]
        ret+= [('-2', 'Direct', 1 if self.current_mode == -2 else 0)]
        ret+= [(x, x+1, 1 if self.current_mode == x else 0) for x in range(self.MODE_COUNT)]
        return ret

    def set_brightness(self, b):
        self.s.set_value("brightness", str(b))
        self.led.set_brightness(int(b))

    def get_brightness(self):
        return self.led.get_brightness()

    def get_animation_list(self):
        return self.ANIMATION_LIST

    def get_animation_list(self):
        l = []
        if self.current_mode >= 0:
            for identifier, name in self.ANIMATION_LIST:
                l.append(('button', name, 'Select', self.ani.get_animation_name() == identifier, identifier, None))
        return l

    def get_argument_list(self):
        l = []
        if self.current_mode >= 0:
            for identifier, name in self.ani.get_animation().get_argument_list():
                l.append(('plusminus', str(name)+str(self.ani.get_animation().get_argument(str(identifier))), None, None, str(identifier)+"_plus", str(identifier)+"_minus"))
        return l

    def change_argument(self, arg_name, arg_diff):
        if self.ani.get_animation().argument_exists(arg_name):
            arg = int(self.ani.get_animation().get_argument(arg_name))
            arg += arg_diff
            self.ani.get_animation().set_argument(arg_name, str(arg))
            arg2 = self.ani.get_animation().get_argument(arg_name) # just in case it didn't pass the min/max thresholds
            self.s.set_value(arg_name, str(arg2), section=str(self.current_mode))

    def get_argument_names(self):
        return self.ani.get_animation().get_argument_names()

    def change_mode(self, mode_number):
        if mode_number < self.MODE_COUNT:
            self.s.set_value("mode", str(mode_number))
            animation = None
            if mode_number == -1:
                animation = "off"
            elif mode_number == -2:
                animation = "direct"
            else:
                animation = self.s.get_value("animation", section=str(mode_number), default="off")
            self.current_mode = mode_number
            self._change_animation(animation, store=False)

    def direct_call(self, data):
        if self.current_mode == -2:
            self.ani.get_animation().direct_call(data)
            return True
        else:
            return False

    def mode_call(self, call):
        if str(call) in [str(identifier) for identifier, x, y in self.get_mode_list()]:
            self.change_mode(int(call))

    def arg_call(self, call):
        if call in [identifier+"_plus" for identifier in self.get_argument_names()]:
            self.change_argument([identifier for identifier in self.get_argument_names() if identifier+"_plus" == call][0], 1)
        elif call in [identifier+"_minus" for identifier in self.get_argument_names()]:
            self.change_argument([identifier for identifier in self.get_argument_names() if identifier+"_minus" == call][0], -1)

    def animation_call(self, call):
        self.change_animation(str(call))
