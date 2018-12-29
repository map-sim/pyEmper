#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

from time import time
from graphSQL import GraphSQL
from configSQL import ConfigSQL
from xiagramSQL import XiagramSQL
from basicToolBox import printInfo


class GlobSimSQL(ConfigSQL):

    def __init__(self, fname):
        self.__startTime = time()
        super(GlobSimSQL, self).__init__(fname)
        self.diagram = XiagramSQL(fname)
        self.graph = GraphSQL(fname)

    def __del__(self):
        super(GlobSimSQL, self).__del__()
        deltaTime = time() - self.__startTime 
        printInfo(f"duration: {deltaTime:.3f} s")
        
    def getNationList(self):
        rows = self.select("nation_st", "name")
        setNations = set([row[0] for row in rows])
        return list(sorted(setNations))
