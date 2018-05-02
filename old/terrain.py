#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

import os
from termcolor import colored

            
class EmpTerrains(dict):
    def __init__(self, world, conf):
        dict.__init__(self)
        self.world = world
        
        for name in conf.keys():
            t = EmpTerrain(name, conf[name])
            self[name] = t
            print(t)        
        print("sum:", len(self))
        print(colored("(new)", "red"), "EmpTerrains")
        
    def get_nearest(self, rgb):
        tmp = [(t - rgb, t) for t in self.values()]
        tmp = min(tmp, key=lambda e: e[0])
        return tmp[1]
    
    def get_conf(self):
        out = {}
        for k in self.keys():
            out[k] = self[k].get_conf()
        return out

    
class EmpTerrain:
    def __init__(self, name, conf):
        self.name = str(name)
        self.conf = conf
        
        if float(conf["conductivity"][0])<0 or float(conf["conductivity"][0])>1:
            raise ValueError("conductivity[0] has wrong value")
        self.con_base = float(conf["conductivity"][0])
        
        if float(conf["conductivity"][1])<0 or float(conf["conductivity"][1])>1:
            raise ValueError("conductivity[1] has wrong value")
        self.con_delta = float(conf["conductivity"][1])
        
        if float(conf["ifc"])<0 or float(conf["ifc"])>1:
            raise ValueError("ifc has wrong value")
        self.infr_cost = float(conf["ifc"])

        if not isinstance(conf["color"], (tuple, list)):
            raise TypeError("no rgb collection")
        self.rgb = tuple([int(c, 16) for c in conf["color"]])

    def __sub__(self, rgb):
        if isinstance(rgb, (EmpTerrain, )):
            rgb = rgb.rgb
        if not isinstance(rgb, (tuple, list)):
            raise TypeError("no rgb collection")

        out = 0
        for i, j in zip(self.rgb, rgb):
            out += abs(i - j)
        return out

    def get_conf(self):
        self.conf["ifc"] = self.infr_cost
        self.conf["color"] = [hex(c) for c in self.rgb]
        self.conf["conductivity"] = [self.con_base, self.con_delta]
        return self.conf
    
    def __str__(self):
        out = self.name + ": "
        out += "%g | " % self.infr_cost
        out += "%g %g | " % (self.con_base, self.con_delta)
        out += "%s %s %s" % tuple([hex(c) for c in self.rgb])
        return out

    def isriver(self):
        return self.con_base >= 0.8

    def isground(self):
        return self.con_base > 0

    def iswater(self):
        return self.con_base == 0
    
