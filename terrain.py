#! /usr/bin/python3

import os

            
class EmpTerrains(dict):
    def __init__(self, conf):
        dict.__init__(self)
        for name in conf.keys():
            t = EmpTerrain(name, conf[name])
            self[name] = t
            print(t)        
        print("sum:", len(self))
        
    def get_conf(self):
        out = {}
        for k in self.keys():
            out[k] = self[k].get_conf()
        return out

    
class EmpTerrain:
    def __init__(self, name, conf):
        self.name = str(name)
        self.conf = conf
        
        if float(conf["CON"][0])<0 or float(conf["CON"][0])>1:
            raise ValueError("CON[0] has wrong value")
        self.con_ground = float(conf["CON"][0])
        
        if float(conf["CON"][1])<0 or float(conf["CON"][1])>1:
            raise ValueError("CON[1] has wrong value")
        self.con_water = float(conf["CON"][1])
        
        if float(conf["IFC"])<0 or float(conf["IFC"])>1:
            raise ValueError("IFC has wrong value")
        self.infr_cost = float(conf["IFC"])

        if not isinstance(conf["RGB"], (tuple, list)):
            raise TypeError("no rgb collection")
        self.rgb = tuple([int(c, 16) for c in conf["RGB"]])

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
        return self.conf
    
    def __str__(self):
        out = self.name + ":\n"
        out += "\t%g\n" % self.infr_cost
        out += "\t%g %g\n" % (self.con_ground, self.con_water)
        out += "\t%s %s %s" % tuple([hex(c) for c in self.rgb])
        return out

    

