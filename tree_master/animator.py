#!/usr/bin/env python2

from threading import Thread

class animator(object):
    def __init__(self, led, storage):
        self.animation = None
        self.name = None
        self.led = led
        self.storage = storage

    # sets animation, returns true if successful
    def set_animation(self, animation_name):
        if animation_name is None:
            self.stop_animation()
            return self.animation is not None
        a = __import__("animations."+animation_name, globals(), locals(), [], -1)
        self.animation = getattr(getattr(a, animation_name), animation_name)(self.led, self.storage)
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

    def get_animation_name(self):
        return self.name

    def get_animation(self):
        return self.animation