#!/usr/bin/env python3

from threading import Thread

class animation(Thread):
    def __init__(self, led, storage, name, blank_args=False):
        super(animation, self).__init__()
        self.led = led
        self.storage = storage
        self.enabled = True
        self.arguments = []
        self.animation_name = name
        
        self.RAMP_UP_MIN = 1
        self.RAMP_UP_MAX = self.led.CONST_MAX_INTENSITY
        self.CALM_DOWN_MIN = 1
        self.CALM_DOWN_MAX = self.led.CONST_MAX_INTENSITY
        self.RETENTION_MIN = 0
        self.RETENTION_MAX = 1000
        
        if not blank_args:
            self.initialize_argument("ramp_up", "Ramp up: ", default_value=20)
            self.led.set_ramp_up_speed(self.get_argument("ramp_up"))
            self.initialize_argument("calm_down", "Calm down: ", default_value=2)
            self.led.set_calm_down_speed(self.get_argument("calm_down"))
            self.initialize_argument("retention", "Retention: ", default_value=10)
            self.led.set_retention(self.get_argument("retention"))
    def disable(self):
        self.enabled = False
    def get_name(self):
        return self.animation_name
    def initialize_argument(self, arg_name, human_readable, default_value=None):
        self.arguments.append((arg_name, human_readable))
        if self.storage.get_value(arg_name, section=self.animation_name) is None:
            self.storage.set_value(arg_name, default_value, section=self.animation_name)
    def set_argument(self, arg_name, arg_value):
        if arg_name in self.get_argument_ids():
            if arg_name == "ramp_up" and arg_value >= self.RAMP_UP_MIN and arg_value <= self.RAMP_UP_MAX:
                self.led.set_ramp_up_speed(arg_value)
            elif arg_name == "ramp_up":
                return
            elif arg_name == "calm_down" and arg_value >= self.CALM_DOWN_MIN and arg_value <= self.CALM_DOWN_MAX:
                self.led.set_calm_down_speed(arg_value)
            elif arg_name == "calm_down":
                return
            elif arg_name == "retention" and arg_value >= self.RETENTION_MIN and arg_value <= self.RETENTION_MAX:
                self.led.set_retention(arg_value)
            elif arg_name == "retention":
                return
            self.storage.set_value(arg_name, arg_value, section=self.animation_name)
    def get_argument_list(self):
        return self.arguments
    def get_argument(self, arg_name):
        if arg_name in self.get_argument_ids():
            return self.storage.get_value(arg_name, section=self.animation_name)
        else:
            return None
    def get_argument_ids(self):
        return [identifier for identifier, name in self.arguments]
