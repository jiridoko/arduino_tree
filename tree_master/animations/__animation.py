#!/usr/bin/env python3

from threading import Thread

class animation(Thread):
    def __init__(self, led, name):
        super(animation, self).__init__()
        self.led = led
        self.enabled = True
        self.arguments = []
        self.animation_name = name
        
    def disable(self):
        self.enabled = False

    def get_name(self):
        return self.animation_name

    def initialize_argument(self, arg_name, human_readable, default_value=None, value=None):
        self.arguments.append((arg_name, human_readable, default_value if value is None else value))

    def set_argument(self, arg_name, arg_value):
        if arg_name in self.get_argument_ids():
            self._store_argument(arg_name, arg_value)

    def _store_argument(self, arg_name, arg_value):
        self.arguments[:] = [(identifier, name, value) if identifier != arg_name else (identifier, name, arg_value) for identifier, name, value in self.arguments]

    def get_argument_names(self):
        return [identifier for identifier, name, value in self.arguments]

    def get_argument_list(self):
        return [(identifier, name) for identifier, name, value in self.arguments]

    def argument_exists(self, arg_name):
        return arg_name in [identifier for identifier, name, value in self.arguments]

    def get_argument(self, arg_name):
        if arg_name in self.get_argument_ids():
            ret = [value for identifier, name, value in self.arguments if identifier == arg_name]
            if len(ret) > 0:
                return ret[0]
            else:
                return None
        else:
            return None

    def get_argument_ids(self):
        return [identifier for identifier, name, value in self.arguments]
