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

    def __init__(self, savedir):

        # check "/" char
        if savedir[-1] != "/": 
            savedir += "/"
            
        # load main config
        with open(savedir + "main.json") as dc:
            self.conf = json.load(dc)
            
        self.terrains = EmpTerrains(self.conf["terrains"])
        self.diagram = EmpDiagram(self.terrains, savedir + self.conf["params"]["diagram"])
        self.network = EmpNetwork(self.diagram, savedir + self.conf["params"]["nodes"])
            
    def save(self, savedir):

        # check "/" char
        if savedir[-1] != "/": 
            savedir += "/"

        self.conf["params"]["nodes"] = "nodes.json"
        self.conf["params"]["diagram"] = "map.ppm"
        
        with open("main.json", "w") as fd:
            json.dump(self.conf, fd)

        self.network.save(savedir, self.conf["params"]["nodes"])
        self.diagram.save(savedir, self.conf["params"]["diagram"])
        print(colored("(info)", "red"), "save config as:", savedir)
