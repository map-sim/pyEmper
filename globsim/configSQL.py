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
        self.__cache = dict()

    def getParam(self, name):
        try:
            return self.__cache[name]
        except KeyError: pass
        
        out = self.select("config_ft", "value", f"name='{name}'")
        try:
            if name in self.intConf:
                value = int(out[0][0])
            else: value = float(out[0][0])
            self.__cache[name] = value
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
        
