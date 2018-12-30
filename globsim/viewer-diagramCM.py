#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

from diagramGTK import DiagramGTK
from basicToolBox import printDebug
from basicToolBox import printWarning
from basicToolBox import printError
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

class DiagramCM(DiagramGTK):    
    def __init__(self, database, offset=0, flags={}):
        super(DiagramCM, self).__init__(database, offset)
        
        self.savx = None
        self.savy = None
        self.tmpNode = None
        self.tmpAngle = None
        self.tmpColor = None
        self.nodeList = []
        
        # basicToolBox.debug = True

        self.getColor = self.handler.diagram.getTerrColor
        self.checkLine = self.handler.diagram.checkBorder
        
        if flags["cmode"]:
            self.checkLine = self.handler.diagram.checkCoast
            self.getColor = self.handler.diagram.getCurrColor        
            self.refrechScreen()                    
        
        if flags["bmode"]:
            self.borderToogle()

        self.refrechScreen()        
        self.show_all()

    def printHelp(self):
        printInfo("1 - draw map of terrains")
        printInfo("2 - draw map of currents")
        printInfo("r - refresh screen (redraw, sync from DB)")
        printInfo("n - create new node with random name")
        printInfo("s - smooth borders (sync to DB)")
        printInfo("b - toogle borders")
        printInfo("u - smooth current diagram (it can takes a few minutes)")
        printInfo("t - print info about terrains (selected is marked by star)")
        printInfo("c - change terrain (go to next)")
        printInfo("q - angule reset")
        printInfo("p - print tmp info")
        printInfo("h - this help")
        
    def onClick(self, box, event):
        if self.getColor == self.handler.diagram.getTerrColor:
            self.onTerrCross(box, event)
        elif self.getColor == self.handler.diagram.getCurrColor:
            self.onCurrCross(box, event)
        else:
            printError("ony 2 modes")
            # self.onROCross(box, event)
                                
    def onPress(self, widget, event):
        printDebug(f"Key val: {event.keyval}")    
        printDebug(f"Key name: {Gdk.keyval_name(event.keyval)}")    

        if Gdk.keyval_name(event.keyval) == "h":
            self.printHelp()
            return
            
        if Gdk.keyval_name(event.keyval) == "1":
            self.checkLine = self.handler.diagram.checkBorder
            self.getColor = self.handler.diagram.getTerrColor        
            self.refrechScreen()
            return
            
        if Gdk.keyval_name(event.keyval) == "2":
            self.checkLine = self.handler.diagram.checkCoast
            self.getColor = self.handler.diagram.getCurrColor        
            self.refrechScreen()                    
            return

        if Gdk.keyval_name(event.keyval) == "r":
            printInfo("refresh screen")
            self.refrechScreen()
            return

        if Gdk.keyval_name(event.keyval) == "t":
            try:
                pattern = rgb2str(self.tmpColor)
            except TypeError: pattern = self.tmpColor
            
            for color in self.handler.diagram.terrains.keys():
                prom = "*" if color == pattern else "-" 
                terr = self.handler.diagram.terrains[color]
                printInfo(f"{prom} {color}: {terr[0]} {terr[1]} {terr[2]}")
            return

        if Gdk.keyval_name(event.keyval) == "b":
            self.borderToogle()
            return
            
        if Gdk.keyval_name(event.keyval) == "c":
            try:
                pattern = rgb2str(self.tmpColor)
            except TypeError:
                colors = self.handler.diagram.terrains.keys()
                self.tmpColor = str2rgb(list(colors)[0])
                return
            
            flag = False
            for color in self.handler.diagram.terrains.keys():
                if flag:
                    self.tmpColor = str2rgb(color)
                    return 
                
                if color == pattern: flag = True
            colors = self.handler.diagram.terrains.keys()
            self.tmpColor = str2rgb(list(colors)[0])
            return
                    
        if Gdk.keyval_name(event.keyval) == "q":
            self.tmpAngle = None
            self.nodeList = []
            return

        if Gdk.keyval_name(event.keyval) == "p":
            printInfo(f"node: {self.tmpNode} color: {self.tmpColor} | angle: {self.tmpAngle}")
            return

        if len(sys.argv) <= 3:
            printWarning("read-only mode!")
            return
        elif len(sys.argv) > 3:
            if sys.argv[3] != "--edit":
                printWarning("read-only mode!")
                return
            
        if Gdk.keyval_name(event.keyval) == "n":
            charset = string.ascii_uppercase
            nodeset = self.handler.diagram.getNodeSet()
            newname = ''.join(random.sample(charset*3, 3))
            while newname in nodeset: 
                newname = ''.join(random.sample(charset*3, 3))
            self.tmpNode = newname
            printInfo(f"new node: {newname}")
            return
            
        if Gdk.keyval_name(event.keyval) == "s":            
            n = self.handler.diagram.smoothBorder()
            printInfo(f"smooth border: {n}")
            return
            
        if Gdk.keyval_name(event.keyval) == "u":
            self.handler.diagram.smoothCurrent(self.nodeList)
            printInfo(f"smooth current...")
            return
            
        printWarning("not defined key!")
            
    def borderToogle(self):
        if self.checkLine == self.handler.diagram.checkCoast:
            self.checkLine = self.handler.diagram.checkBorder
        else: self.checkLine = self.handler.diagram.checkCoast
        self.refrechScreen()                    
        printInfo("toogle border")
            
    def onCurrCross(self, box, event):            
        x, y = self.extractXY(event)
        
        if event.button == 2:
            self.nodeList.append(self.handler.diagram[x,y][0])
            printInfo(self.nodeList)            
            printInfo("refresh screen")            
            self.refrechScreen()
            return

        if len(sys.argv) <= 3:
            printWarning("read-only mode!")
            return
        elif len(sys.argv) > 3:
            if sys.argv[3] != "--edit":
                printWarning("read-only mode!")
                return
        
        if event.button == 1:
            self.savx = x
            self.savy = y
            if self.tmpAngle is None:
                n,t,dx,dy = self.handler.diagram[self.savx,self.savy]
                self.handler.diagram[self.savx, self.savy] = n,t,0,0
                n,t,dx,dy = self.handler.diagram[self.savx+1,self.savy]
                self.handler.diagram[self.savx+1, self.savy] = n,t,0,0            
                n,t,dx,dy = self.handler.diagram[self.savx-1,self.savy]
                self.handler.diagram[self.savx-1, self.savy] = n,t,0,0            
                n,t,dx,dy = self.handler.diagram[self.savx,self.savy+1]
                self.handler.diagram[self.savx, self.savy+1] = n,t,0,0
                n,t,dx,dy = self.handler.diagram[self.savx,self.savy-1]
                self.handler.diagram[self.savx, self.savy-1] = n,t,0,0
                return

        if event.button == 3:
            if self.savx is None or  self.savy is None: return
            self.tmpAngle = math.atan2(self.savy-y, self.savx-x)
            printDebug("new angle")            
            
        if self.value > 1: radius = 1
        else: radius = self.value
        
        n,t,dx,dy = self.handler.diagram[self.savx,self.savy]
        dy = -radius * math.sin(self.tmpAngle)
        dx = radius * math.cos(self.tmpAngle)
        printDebug("dx: {}".format(dx))
        printDebug("dy: {}".format(dy))

        self.handler.diagram[self.savx, self.savy] = n,t,dx,dy
        n,t,dxo,dyo = self.handler.diagram[self.savx+1,self.savy]
        self.handler.diagram[self.savx+1, self.savy] = n,t,dx,dy
        n,t,dxo,dyo = self.handler.diagram[self.savx-1,self.savy]
        self.handler.diagram[self.savx-1, self.savy] = n,t,dx,dy
        val = self.handler.diagram[self.savx,self.savy+1]
        if val: self.handler.diagram[self.savx, self.savy+1] = val[0],val[1],dx,dy        
        val = self.handler.diagram[self.savx,self.savy-1]
        if val: self.handler.diagram[self.savx, self.savy-1] = val[0],val[1],dx,dy
        
    def onTerrCross(self, box, event):            
        if event.button == 2:
            printInfo("refresh screen")
            self.refrechScreen()
            return
        x, y = self.extractXY(event)
        
        if event.button == 3:
            self.tmpNode = self.handler.diagram.getNode(x,y)
            self.tmpColor = self.handler.diagram.getTerrColor(x,y)
            area = self.handler.diagram.calcArea(self.tmpNode)
            mx, my = self.handler.diagram.calcMean(self.tmpNode)
            capacity = self.handler.diagram.calcCapacity(self.tmpNode)
            aperture = self.handler.diagram.calcAperture(self.tmpNode)
            charge = self.handler.diagram.calcCharge(self.tmpNode)
            info = f"area: {area} aperture: {aperture} capacity: {capacity} charge: {charge}"
            printInfo(f"node: {self.tmpNode} {info} | {int(mx)}x{int(my)} color: {self.tmpColor}")

        if len(sys.argv) <= 3:
            printWarning("read-only mode!")
            return
        elif len(sys.argv) > 3:
            if sys.argv[3] != "--edit":
                printWarning("read-only mode!")
                return
        
        if event.button == 1:
            if not self.tmpNode: return
            if not self.tmpColor: return
            nt = self.tmpNode, rgb2str(self.tmpColor)
            self.handler.diagram[x, y] = nt
            self.handler.diagram[x+1, y] = nt
            self.handler.diagram[x-1, y] = nt
            self.handler.diagram[x, y+1] = nt
            self.handler.diagram[x, y-1] = nt
                                        
try:
    flags = {}
    if "c" in sys.argv[2]:
        flags["cmode"] = True
    else: flags["cmode"] = False      
    if "b" in sys.argv[2]: 
        flags["bmode"] = True
    else: flags["bmode"] = False
    
    fregexp = lambda x: re.search("[0-9]", x)
    filtered = filter(fregexp, sys.argv[2])
    offset = int("".join(list(filtered)))
    
    win = DiagramCM(sys.argv[1], offset, flags)
    
except IndexError:
    flags = {"cmode": False, "bmode": False}
    win = DiagramCM(sys.argv[1], flags=flags)

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
