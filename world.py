#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from terrain import EmpTerrains 
from diagram import EmpDiagram 
from network import EmpNetwork 
from nation import EmpNation

from termcolor import colored

import time
import json
import os

class EmpWorld:

    def __init__(self, savedir):

        # check "/" char
        if savedir[-1] != "/": 
            savedir += "/"
            
        # load main config
        with open(savedir + "main.json") as dc:
            self.conf = json.load(dc)
            
        self.terrains = EmpTerrains(self, self.conf["terrains"])
        self.diagram = EmpDiagram(self.terrains, savedir + self.conf["diagram"])
        self.network = EmpNetwork(self.diagram, savedir + self.conf["nodes"])
            
        self.nations = {}
        for name in self.conf["nations"].keys():
            self.nations[name] = EmpNation(name, self.conf["nations"][name])

                    
    def save(self, savedir):

        # check "/" char
        if savedir[-1] != "/": 
            savedir += "/"

        self.conf["nodes"] = "nodes.json"
        self.conf["diagram"] = "map.ppm"
        self.conf["terrains"] = self.terrains.get_conf()
        
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        else:
            warning = colored("(warning)", "yellow")
            print(warning, "dir %s exists!" % savedir)

        with open(savedir +"main.json", "w") as fd:
            json.dump(self.conf, fd)

        self.network.save(savedir + self.conf["nodes"])
        self.diagram.save(savedir + self.conf["diagram"])
        print(colored("(info)", "red"), "save config as:", savedir)
