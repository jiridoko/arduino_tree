#!/usr/bin/env python2

from threading import Thread

class animation(Thread):
    def __init__(self, led, storage, name, blank_args=False):
        super(animation, self).__init__()
        self.led = led
        self.storage = storage
        self.enabled = True
        self.arguments = []
        self.animation_name = name
        if not blank_args:
            self.initialize_argument("ramp_up", default_value=20)
            self.led.set_ramp_up_speed(self.get_argument("ramp_up"))
            self.initialize_argument("calm_down", default_value=2)
            self.led.set_calm_down_speed(self.get_argument("calm_down"))
            self.initialize_argument("retention", default_value=10)
            self.led.set_retention(self.get_argument("retention"))
    def disable(self):
        self.enabled = False
    def initialize_argument(self, arg_name, default_value=None):
        self.arguments.append(arg_name)
        if self.storage.get_value(arg_name, section=self.animation_name) is None:
            self.storage.set_value(arg_name, default_value, section=self.animation_name)
    def set_argument(self, arg_name, arg_value):
        if arg_name in self.arguments:
            self.storage.set_value(arg_name, arg_value, section=self.animation_name)
    def get_argument_list(self):
        return self.arguments
    def get_argument(self, arg_name):
        if arg_name in self.arguments:
            return self.storage.get_value(arg_name, section=self.animation_name)
        else:
            return None
    def set_ramp_up(self, value):
        if "ramp_up" in self.arguments:
            self.set_argument("ramp_up", value)
            self.led.set_ramp_up_speed(value)
    def set_calm_down(self, value):
        if "calm_down" in self.arguments:
            self.set_argument("calm_down", value)
            self.led.set_calm_down_speed(value)
    