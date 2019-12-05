#!/usr/bin/env python3

from threading import Semaphore

class Colour(object):
    def __init__(self, red=0, green=0, blue=0, intensity=255):
        self.red = red
        self.green = green
        self.blue = blue
        self.intensity = intensity
        self.diff_red = 0
        self.diff_green = 0
        self.diff_blue = 0
        self.diff_intensity = 0
        self.outstanding_steps_r = 0
        self.outstanding_steps_g = 0
        self.outstanding_steps_b = 0
        self.outstanding_steps_i = 0
        self.semaphore = Semaphore()
    def __bool__(self):
        if self.intensity == 0 or (self.red == 0 and self.green == 0 and self.blue == 0):
            return False
        return True
    def __eq__(self, other):
        return self.red == other.red and self.blue == other.blue and self.green == other.green and self.intensity == other.intensity
    def __ne__(self, other):
        return self.red != other.red or self.blue != other.blue or self.green != other.green or self.intensity != other.intensity
    def __byte_safe(self, n):
        if n < 0:
            return 0
        elif n > 255:
            return 255
        else:
            return round(n)
    def get_red(self):
        return self.__byte_safe(self.red*(self.intensity/255))
    def get_green(self):
        return self.__byte_safe(self.green*(self.intensity/255))
    def get_blue(self):
        return self.__byte_safe(self.blue*(self.intensity/255))
    def get(self):
        with self.semaphore:
            return [self.get_red(), self.get_green(), self.get_blue()]
    def set_red(self, red):
        self.red = __byte_safe(red)
    def set_green(self, green):
        self.green = __byte_safe(green)
    def set_blue(self, blue):
        self.blue = __byte_safe(blue)
    def set_intensity(self, intensity):
        self.intensity = __byte_safe(intensity)
    def set(self, red=None, green=None, blue=None, intensity=None):
        with self.semaphore:
            if red is not None:
                self.red = self.__byte_safe(red)
                self.diff_red = 0
                self.outstending_steps_r = 0
            if green is not None:
                self.green = self.__byte_safe(green)
                self.diff_green = 0
                self.outstending_steps_g = 0
            if blue is not None:
                self.blue = self.__byte_safe(blue)
                self.diff_blue = 0
                self.outstending_steps_b = 0
            if intensity is not None:
                self.intensity = self.__byte_safe(intensity)
                self.diff_intensity = 0
                self.outstending_steps_i = 0
    def set_soft(self, red=None, green=None, blue=None, intensity=None, steps=0):
        with self.semaphore:
            if steps < 0:
                return
            if red is not None:
                self.diff_red = (red-(self.red*1.0))/(steps+1)
                self.outstanding_steps_r = steps
            if green is not None:
                self.diff_green = (green-(self.green*1.0))/(steps+1)
                self.outstanding_steps_g = steps
            if blue is not None:
                self.diff_blue = (blue-(self.blue*1.0))/(steps+1)
                self.outstanding_steps_b = steps
            if intensity is not None:
                self.diff_intensity = (intensity-(self.intensity*1.0))/(steps+1)
                self.outstanding_steps_i = steps
    def update(self):
        with self.semaphore:
            if self.outstanding_steps_r > 0:
                self.red+=self.diff_red
                self.outstanding_steps_r-=1

            if self.outstanding_steps_g > 0:
                self.green+=self.diff_green
                self.outstanding_steps_g-=1

            if self.outstanding_steps_b > 0:
                self.blue+=self.diff_blue
                self.outstanding_steps_b-=1

            if self.outstanding_steps_i > 0:
                self.intensity+=self.diff_intensity
                self.outstanding_steps_i-=1

if __name__ == "__main__":
    c1=Colour()
    c2=Colour(red=25)
    c3=Colour(green=150, red=15, intensity=0)
    c4=Colour(green=150, red=15, intensity=0)
    print(str(bool(c1)))
    print(str(bool(c2)))
    print(str(bool(c3)))
    print(str(c4==c3))
