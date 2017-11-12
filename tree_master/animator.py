#!/usr/bin/env python2

from threading import Thread

class animator(object):
    def __init__(self, led):
        self.animation = None
        self.name = None
        self.led = led

    # sets animation, returns true if successful
    def set_animation(self, animation_name):
        a = __import__("animations."+animation_name, globals(), locals(), [], -1)
        self.animation = getattr(getattr(a, animation_name), animation_name)(self.led)
        self.name = animation_name
        return self.animation is not None

    def start_animation(self):
        if self.animation is not None:
            self.animation.start()

    def stop_animation(self):
        if self.animation is not None:
            self.animation.disable()
            del self.animation
            self.animation = None
            self.name = None
