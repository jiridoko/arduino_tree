#!/usr/bin/env python3

from . import __animation

class off(__animation.animation):
    def __init__(self, led, storage):
        super(off, self).__init__(led, storage, "off", blank_args=True)
    def run(self):
        pass
