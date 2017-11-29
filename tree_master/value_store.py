#!/usr/bin/env python3

import configparser
import os

class storage(object):
    def __init__(self, filename):
        self.filename = filename
        self.c = configparser.ConfigParser()
        self._load()

    def _load(self):
        if os.path.isfile(self.filename):
            self.c.read(self.filename)

    def _store(self):
        with open(self.filename, 'w') as f:
            self.c.write(f)
            
    def _ConfigSectionMap(self, section):
        dict1 = {}
        try:
            options = self.c.options(section)
            for option in options:
                try:
                    dict1[option] = self.c.get(section, option)
                    if dict1[option] == -1:
                        pass
                except:
                    dict1[option] = None
        except configparser.NoSectionError:
            dict1[section] = None
        return dict1

    def set_value(self, name, value, section="main"):
        try:
            options = self.c.options(section)
        except:
            self.c.add_section(section)
        self.c.set(section, name, str(value))
        self._store()

    def get_value(self, name, default=None, section="main"):
        retval = default
        try:
            retval = self._ConfigSectionMap(section)[name]
        except KeyError:
            return default
        return retval

if __name__ == "__main__":
    s = storage('test2.out')
    print(str(s.get_value("test")))
    s.set_value("test", "val")
    print(str(s.get_value("test")))
    s.set_value("test2", 56)
    print(str(int(s.get_value("test2"))+2))
