#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

from configSQL import ConfigSQL
from eDiagramSQL import eDiagramSQL
from globsimTools import printInfo
from time import time


class GlobSimSQL(ConfigSQL):

    def __init__(self, fname):
        self.__startTime = time()
        super(GlobSimSQL, self).__init__(fname)
        self.diagram = eDiagramSQL(fname)
                    
    def __del__(self):
        super(GlobSimSQL, self).__del__()
        deltaTime = time() - self.__startTime 
        printInfo(f"duration: {deltaTime:.3f} s")

