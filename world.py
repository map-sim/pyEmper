#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from terrain import EmpTerrains 
from diagram import EmpDiagram 
from network import EmpNetwork 

from termcolor import colored

import json

class EmpWorld:

    def __init__(self, fname):

        with open(fname) as dc:
            self.conf = json.load(dc)

        self.terrains = EmpTerrains(self.conf["terrains"])
        self.diagram = EmpDiagram(self.terrains, self.conf["params"]["diagram"])
        self.network = EmpNetwork(self.diagram, self.conf["params"]["nodes"])
            
    def save(self, preffix):
        suffppm = "-map.ppm"
        suffnodes = "-nodes.json"
        suffconf = "-config.json"

        self.conf["params"]["nodes"] = preffix + suffnodes
        self.conf["params"]["diagram"] = preffix + suffppm
        
        fname = preffix + suffconf
        with open(fname, "w") as fd:
            json.dump(self.conf, fd)
        print(colored("(info)", "red"), "save config as:", fname)
        self.network.save(preffix+suffnodes)
        self.diagram.save(preffix+suffppm)
