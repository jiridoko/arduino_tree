#!/usr/bin/env python2

from threading import Thread

class animation(Thread):
    def __init__(self, led):
        super(animation, self).__init__()
        self.led = led
        self.enabled = True
    def disable(self):
        self.enabled = False
