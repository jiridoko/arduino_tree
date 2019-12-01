#!/usr/bin/env python3
from threading import Thread
import time
import spidev
import ws2812
from colour import Colour

class led_master(Thread):
    CONST_LED_COUNT = 150

    def __init__(self, delay=0):
        super(led_master, self).__init__()
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.diodes = self.__initialise_diodes()
        self.delay = delay
        self.updating = True
        self.brightness = 255
        self.c = 0

    def __initialise_diodes(self):
        a = []
        for i in range(self.CONST_LED_COUNT):
            new_item = Colour()
            a.append(new_item)
        return a

    def set_delay(self, delay):
        self.delay = delay

    def set_updating(self, value):
        self.updating = value

    def set_brightness(self, b):
        self.brightness = int(b)
        for i in range(self.CONST_LED_COUNT):
            self.diodes[i].set_soft(intensity=b, steps=10)

    def get_brightness(self):
        return int(self.brightness)

    def get_diode(self, diode_id):
        if diode_id < self.CONST_LED_COUNT:
            return self.diodes[diode_id]
        else:
            return None

    def get_array(self):
        return [x.get() for x in self.diodes]

    def counter(self, d):
        print("run: "+str(self.c)+", delay: "+str(d)+", d1: "+str(self.diodes[0].get())+" "+str(self.diodes[0].diff_red)+", o: "+str(self.diodes[0].outstanding_steps))
        print(str(self.get_array()))
        self.c+=1

    def run(self):
        while self.updating:
            for i in range(0,self.CONST_LED_COUNT):
                self.diodes[i].update()
            ws2812.write2812(self.spi, self.get_array())
            #self.counter(self.delay)
            time.sleep(self.delay)

if __name__ == "__main__":
    from time import sleep
    import sys

    l = led_master(delay=0)

    try:
        l.start()

        sleep(1)

        for i in range(20):
            for j in range(0, 150):
                l.get_diode(j).set_soft(red=255, green=0, blue=0, steps=30, intensity=50)
            sleep(3)
            for j in range(0, 150):
                l.get_diode(j).set_soft(red=255, green=255, blue=0, steps=30, intensity=50)
            sleep(3)
            for j in range(0, 150):
                l.get_diode(j).set_soft(red=0, green=255, blue=0, steps=30, intensity=50)
            sleep(3)
            for j in range(0, 150):
                l.get_diode(j).set_soft(red=0, green=255, blue=255, steps=30, intensity=50)
            sleep(3)
            for j in range(0, 150):
                l.get_diode(j).set_soft(red=0, green=0, blue=255, steps=30, intensity=50)
            sleep(3)
            for j in range(0, 150):
                l.get_diode(j).set_soft(red=255, green=0, blue=255, steps=30, intensity=50)
            sleep(3)
        l.set_updating(False)
    except KeyboardInterrupt:
        l.set_updating(False)

