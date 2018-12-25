#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

from basicSQL import BasicSQL
from basicToolBox import printError
from basicToolBox import printInfo


class ConfigSQL(BasicSQL):

    intConf = [
        "map_width",
        "map_height",
        "map_project"
    ]
    
    def __init__(self, fname):
        super(ConfigSQL, self).__init__(fname)

    def printAllParams(self):
        out = self.select("config_ft", "name,value", extra="ORDER BY name")
        for item in out:
            if item[0] in self.intConf:
                printInfo(f"{item[0]} = {int(item[1])}")
            else: printInfo(f"{item[0]} = {item[1]}")
            
    def getParam(self, name):
        
        out = self.select("config_ft", "value", f"name='{name}'")
        try:
            if name in self.intConf:
                value = int(out[0][0])
            else: value = float(out[0][0])
            return value
        
        except IndexError:
            printError(f"no param: {name}")
            raise IndexError
        
    def setParam(self, name, value):
        try:
            val = self.getParam(name)
            self.update("config_ft", f"value={value}", f"name='{name}'")
            
        except IndexError:            
            self.insert("config_ft", f"'{name}',{value}")
            
    def requireMapProjection(self, code):
        project = self.getParam("map_project")
        if project != code:
            printError("wrong projection type!")
            raise ValueError
        printInfo(f"map projection type: {code}")
        
