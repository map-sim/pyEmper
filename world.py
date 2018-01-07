
from terrain import EmpTerrains 
from loader import EmpDiagramLoader 
from saver import EmpSaver

import json

class EmpWorld:

    def __init__(self, fname):
        dc = open(fname)
        conf = json.load(dc)

        self.terrains = EmpTerrains(conf["terrains"])
        loader = EmpDiagramLoader(self.terrains, conf["params"])
        
        self.diagram = loader.get_diagram()
        self.params = conf["params"]
        
        
    def get_cost_to_ground(self, a1, a2):
        cost = abs(a2.t.con_water - a1.t.con_water)
        cost *= self.params["transshipment cost"]
        cost += (1.0 - a2.t.con_ground) * self.params["transport cost"]
        return cost
    
    def save(self, preffix):
        saver = EmpSaver()
        suffppm = "-map.ppm"
        suffjson = "-config.json"
        
        saver["params"] = self.params
        saver["terrains"] = self.terrains
        saver["params"]["diagram ppm"] = preffix + suffppm
        
        saver.save_diagram(self.diagram)
        saver.save(preffix + suffjson)
