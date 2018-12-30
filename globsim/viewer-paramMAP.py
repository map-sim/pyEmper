#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

from diagramGTK import DiagramGTK
from basicToolBox import printDebug
from basicToolBox import printWarning
from basicToolBox import printInfo
from basicToolBox import rgb2str
from basicToolBox import str2rgb

import basicToolBox
import sys, gi, re
import random
import string
import math

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ParamMAP(DiagramGTK):    
    def __init__(self, database, offset=0, flags={}):
        super(ParamMAP, self).__init__(database, offset)
        self.checkLine = self.handler.diagram.checkBorder
                
        # basicToolBox.debug = True
        
        self.modes = ["nation_sm"]
        self.allNodes = self.handler.diagram.getNodeSet()

        self.__goCache = {}
        try:
            self.newMode(sys.argv[4], sys.argv[5])
        except IndexError:
            self.modecount = 0
            self.itemcount = 0
            self.newMode()
        
        self.tmpNode = None        
        self.refrechScreen()        
        self.show_all()

    def onClick(self, box, event):
        if event.button == 2:
            printInfo("refresh screen")
            self.refrechScreen()
            self.value = 1.0
            return

        x, y = self.extractXY(event)
        self.tmpNode = self.handler.diagram.getNode(x,y)
        item = self.tmpItems[self.itemcount]

        if event.button == 3:
            self.value = self.__nodeCache[self.tmpNode, item]
            capacity = self.handler.diagram.calcCapacity(self.tmpNode)
            printInfo(f"node: {self.tmpNode} | {item}: {self.value} ~ {self.value/capacity}")
        
        if len(sys.argv) <= 3:
            printWarning("read-only mode!")
            return
        elif len(sys.argv) > 3:
            if sys.argv[3] != "--edit":
                printWarning("read-only mode!")
                return
        
        if event.button == 1:
            self.handler.graph[self.tmpNode, item] = self.value
            self.__nodeCache[self.tmpNode, item] = self.value
            if self.maxValue < self.value:
                self.maxValue = self.value
            
    def onPress(self, widget, event):
        printInfo(f"Key val: {event.keyval}")    
        printDebug(f"Key name: {Gdk.keyval_name(event.keyval)}")    

        if Gdk.keyval_name(event.keyval) == "i":
            printInfo(f"mode: {self.modes[self.modecount]}")
            printInfo(f"item: {self.tmpItems[self.itemcount]}")
            return
        if Gdk.keyval_name(event.keyval) == "l":
            printInfo(f"mode: {self.modes[self.modecount]}")
            for i,item in enumerate(self.tmpItems):
                printInfo(f"{i}: {item}")                
            return

        if int(event.keyval) == 65362:
            self.itemcount += 1 + len(self.tmpItems)
            self.itemcount %= len(self.tmpItems)
            printInfo(self.tmpItems[self.itemcount])
            self.refrechScreen()
        if int(event.keyval) == 65364:
            self.itemcount += -1 + len(self.tmpItems)
            self.itemcount %= len(self.tmpItems)
            printInfo(self.tmpItems[self.itemcount])
            self.refrechScreen()

        if int(event.keyval) == 65363:
            self.modecount += 1 + len(self.modes)
            self.modecount %= len(self.modes)
            printInfo(self.modes[self.modecount])
            self.newMode()
            self.refrechScreen()
        if int(event.keyval) == 65361:
            self.modecount += -1 + len(self.modes)
            self.modecount %= len(self.modes)
            printInfo(self.modes[self.modecount])
            self.newMode()
            self.refrechScreen()
                        
        if len(sys.argv) <= 3:
            printWarning("read-only mode!")
            return
        elif len(sys.argv) > 3:
            if sys.argv[3] != "--edit":
                printWarning("read-only mode!")
                return
        
        if Gdk.keyval_name(event.keyval) == "n":
            if self.modes[self.modecount] != "nation_sm": return

            cache = {}
            for node in self.allNodes:
                capacity = self.handler.diagram.calcCapacity(node)
                if capacity == 0:                     
                    for nation in self.tmpItems:
                        self.handler.graph[node, nation] = 0
                    continue

                total = 0.0
                for nation in self.tmpItems:
                    share = self.handler.graph[node, nation]
                    total += share
                    
                for nation in self.tmpItems:
                    val = capacity * self.handler.graph[node, nation] / total
                    self.handler.graph[node, nation] = val
                    try: cache[nation] += val
                    except KeyError:
                        cache[nation] = val
                        
                printInfo(f"{node}: {total}")
                
            printInfo("nations:")
            for nation in cache.keys():
                printInfo(f"{nation}: {cache[nation]}")
            self.newMode()
            
        if Gdk.keyval_name(event.keyval) == "m":
            if self.modes[self.modecount] != "nation_sm": return
            nation = self.tmpItems[self.itemcount]
            cacheOut = {}
            counter = 0.0
            
            for node in self.allNodes:
                base = self.__nodeCache[node, nation]
                if base == 0.0: continue

                cache = {}
                vic = self.handler.diagram.getVicinity(node)
                printInfo(f"{vic}")
                for n in vic:
                    try: c = self.__goCache[node, n]
                    except KeyError:
                        c = 1.0 / self.handler.diagram.calcEnterResistance([node], n)
                        printInfo(f"{node} --> {n} = {c}")
                        self.__goCache[node, n] = c 
                    cache[n] = c
                weight = sum(cache.values())
                    
                for n in cache.keys():
                    delta = base * cache[n] / weight
                    try: cacheOut[n] += delta
                    except KeyError: cacheOut[n] = delta
                      
            printInfo(f"deltas: {len(cacheOut)}")
            for node in cacheOut.keys():
                self.__nodeCache[node, nation] += cacheOut[node]
                value = self.__nodeCache[node, nation]
                counter += value

                self.handler.graph[node, nation] += value
                newval = self.handler.graph[node, nation]
                if self.maxValue < newval:
                    self.maxValue = newval
            printInfo(f"delta: {counter}")
            return
        
    def newMode(self, mode=None, item=None):
        if not mode is None:
            self.modecount = self.modes.index(mode)
            
        self.handler.graph.change_table(self.modes[self.modecount])
        if self.modes[self.modecount] == "nation_sm":
            self.tmpItems = self.handler.getNationList()
        else: printError("newMode")

        if not item is None:
            self.itemcount = self.tmpItems.index(item)
        else: self.itemcount %= len(self.tmpItems)
        
        self.__nodeCache = {}
        table = self.modes[self.modecount]
        rows = self.handler.select(table)
        self.maxValue = 0
        for row in rows: 
            node = row["node"]
            for key in self.tmpItems:
                self.__nodeCache[node, key] = float(row[key])
                if self.maxValue < float(row[key]):
                    self.maxValue = float(row[key])
        
    def getColor(self, x, y):
        node = self.handler.diagram.getNode(x,y)
        if self.handler.diagram.isLand(x, y):
            output = 0, 255, 200
        else: output = 0, 200, 255
        item = self.tmpItems[self.itemcount]
        val = self.__nodeCache[node, item]
        if val <= 0: return output
        
        nval = 1.0 - val / self.maxValue
        output = 255, int(255 * nval), int(255 * nval)            
        return output
    
    def printHelp(self):
        printInfo("...")
        
try:    
    fregexp = lambda x: re.search("[0-9]", x)
    filtered = filter(fregexp, sys.argv[2])
    offset = int("".join(list(filtered)))
    
    win = ParamMAP(sys.argv[1], offset)
    
except IndexError:
    win = ParamMAP(sys.argv[1], 0)

if len(sys.argv) > 3:
    fname = sys.argv[3]
    if re.search("^.*[.](png|PNG)$", fname):
        pb = win.img.get_pixbuf()
        pb.savev(fname, "png", "", "")
        printInfo(f"save as: {fname}")
        sys.exit(0)
        
try: Gtk.main()
except KeyboardInterrupt:
    printInfo("break by keyboard")
