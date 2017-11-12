#!/usr/bin/env python2

from time import sleep
import __animation
from random import randint

class snow(__animation.animation):
    def __init__(self, led):
        super(snow, self).__init__(led)
        self.master_snowflake = None
        self._initialize_snowflakes()
        self.snowflakes = []
        self.MAX_SNOWFLAKES = 3
    def _add_snowflake(self):
        if len(self.snowflakes) < self.MAX_SNOWFLAKES:
            self.snowflakes.append(self.master_snowflake)
    def _move_snowflakes(self):
        for i in xrange(0,len(self.snowflakes)):
            next_snowflake = self.snowflakes[i].next_leaf()
            if next_snowflake is None:
                self.snowflakes.remove(self.snowflakes[i])
                continue
            self.snowflakes[i] = next_snowflake
    def run(self):
        counter = 0
        while self.enabled:
            for i in self.snowflakes:
                index = i.get_index()
                if i is not None:
                    self.led.set_led_value(i.get_index(), self.led.CONST_MAX_INTENSITY)
            self._move_snowflakes()
            counter+=1
            if counter == 10:
                counter = 0
                self._add_snowflake()
            sleep(0.05)
            if not self.enabled:
                break

    class snowflake(object):
        def __init__(self, index, next_list):
            self.index = index
            self.next_list = next_list
            self.list_length = len(next_list)
        def is_leaf(self):
            return self.list_length == 0
        def next_leaf(self):
            if self.is_leaf():
                return None
            r = randint(0, self.list_length-1)
            return self.next_list[r]
        def get_index(self):
            return self.index

    def _initialize_snowflakes(self):
        sf79 = self.snowflake(79, [])
        sf78 = self.snowflake(78, [])
        sf77 = self.snowflake(77, [])
        sf76 = self.snowflake(76, [])
        sf75 = self.snowflake(75, [])
        sf74 = self.snowflake(74, [])
        sf73 = self.snowflake(73, [])
        sf72 = self.snowflake(72, [])
        sf71 = self.snowflake(71, [])
        sf70 = self.snowflake(70, [])
        sf69 = self.snowflake(69, [])
        sf68 = self.snowflake(68, [])
        sf67 = self.snowflake(67, [])

        sf66 = self.snowflake(66, [sf79, sf78])
        sf65 = self.snowflake(65, [sf77, sf76])
        sf64 = self.snowflake(64, [sf75, sf74])
        sf63 = self.snowflake(63, [sf73, sf72])
        sf62 = self.snowflake(62, [sf71, sf70])
        sf61 = self.snowflake(61, [sf69, sf68])
        sf60 = self.snowflake(60, [sf67])

        sf59 = self.snowflake(59, [sf66, sf65])
        sf58 = self.snowflake(58, [sf64, sf63])
        sf57 = self.snowflake(57, [sf62, sf61])
        sf56 = self.snowflake(56, [sf60])

        sf55 = self.snowflake(55, [sf59, sf58])
        sf54 = self.snowflake(54, [sf57, sf56])

        sf53 = self.snowflake(53, [sf55, sf54])

        sf52 = self.snowflake(52, [sf53])

        sf51 = self.snowflake(51, [sf52])
        sf50 = self.snowflake(50, [sf51])
        sf49 = self.snowflake(49, [sf50])
        sf48 = self.snowflake(48, [sf49])
        sf47 = self.snowflake(47, [sf48])
        sf46 = self.snowflake(46, [sf47])
        sf45 = self.snowflake(45, [sf46])
        sf44 = self.snowflake(44, [sf45])
        sf43 = self.snowflake(43, [sf44])
        sf42 = self.snowflake(42, [sf43])
        sf41 = self.snowflake(41, [sf42])
        sf40 = self.snowflake(40, [sf41])
        sf39 = self.snowflake(39, [sf40])
        sf38 = self.snowflake(38, [sf39])
        sf37 = self.snowflake(37, [sf38])
        sf36 = self.snowflake(36, [sf37])
        sf35 = self.snowflake(35, [sf36])
        sf34 = self.snowflake(34, [sf35])
        sf33 = self.snowflake(33, [sf34])
        sf32 = self.snowflake(32, [sf33])
        sf31 = self.snowflake(31, [sf32])
        sf30 = self.snowflake(30, [sf31])
        sf29 = self.snowflake(29, [sf30])
        sf28 = self.snowflake(28, [sf29])
        sf27 = self.snowflake(27, [sf28])
        sf26 = self.snowflake(26, [sf27])
        sf25 = self.snowflake(25, [sf26])
        sf24 = self.snowflake(24, [sf25])
        sf23 = self.snowflake(23, [sf24])
        sf22 = self.snowflake(22, [sf23])
        sf21 = self.snowflake(21, [sf22])
        sf20 = self.snowflake(20, [sf21])
        sf19 = self.snowflake(19, [sf20])
        sf18 = self.snowflake(18, [sf19])
        sf17 = self.snowflake(17, [sf18])
        sf16 = self.snowflake(16, [sf17])
        sf15 = self.snowflake(15, [sf16])
        sf14 = self.snowflake(14, [sf15])
        sf13 = self.snowflake(13, [sf14])
        sf12 = self.snowflake(12, [sf13])
        sf11 = self.snowflake(11, [sf12])
        sf10 = self.snowflake(10, [sf11])
        sf9  = self.snowflake(9, [sf10])
        sf8  = self.snowflake(8, [sf9])
        sf7  = self.snowflake(7, [sf8])
        sf6  = self.snowflake(6, [sf7])
        sf5  = self.snowflake(5, [sf6])
        sf4  = self.snowflake(4, [sf5])
        sf3  = self.snowflake(3, [sf4])
        sf2  = self.snowflake(2, [sf3])
        sf1  = self.snowflake(1, [sf2])
        sf0  = self.snowflake(0, [sf1])

        self.master_snowflake = self.snowflake(-1, [sf0])
