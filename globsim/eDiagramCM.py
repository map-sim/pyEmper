#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM


from globsimSQL import GlobSimSQL
from globsimTools import printDebug
from globsimTools import printInfo
from globsimTools import rgb2str
from globsimTools import str2rgb

import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf as Gpb

gi.require_version('GLib', '2.0')
from gi.repository import GLib

class DiagramViewer(Gtk.Window):
    borderRGB = 0, 0, 0
    
    def __init__(self, database, offset=0):
        Gtk.Window.__init__(self, title="EMPER - TMAP VIEWER")
        self.connect("key-press-event",self.onPress)
        self.connect("delete-event", self.onExit)

        self.resize = 2
        self.value = 1.0
        self.database = str(database)        
        self.handler = GlobSimSQL(database)

        self.width = self.handler.getParam("map_width")
        self.height = self.handler.getParam("map_height")
        project = self.handler.getParam("map_project")
        self.handler.requireMapProjection(0)

        fix = Gtk.Fixed()
        self.add(fix)

        ebox = Gtk.EventBox()
        fix.put(ebox, 0,0)

        self.onClick = self.onCross
        ebox.connect('scroll-event', self.onScroll)
        ebox.connect ('button-press-event', self.onClick)
        ebox.add_events(Gdk.EventMask.SCROLL_MASK|Gdk.EventMask.SMOOTH_SCROLL_MASK)
        
        self.img = Gtk.Image()
        ebox.add(self.img)

        self.offset = offset
        self.refrechScreen()        
        self.show_all()

    def refrechScreen(self):        
        diagramRGB = []
        for y in range(self.height):
            top, flo = [], []            
            for x in range(self.width):
                x = (x + self.offset) % self.width
                flag = self.handler.diagram.checkBorder(x, y)
                rgb = self.handler.diagram.getColor(x,y)
                
                lu = self.borderRGB if flag & 8 else rgb 
                ru = self.borderRGB if flag & 1 else rgb 

                row = [*lu, *ru]
                top.extend(2 * self.borderRGB if flag & 2 else row)
                flo.extend(2 * self.borderRGB if flag & 4 else row)
                
            diagramRGB.extend(top)
            diagramRGB.extend(flo)
            
        tmp = GLib.Bytes.new(diagramRGB)
        rowarg = self.resize * 3 * self.width
        confargs = tmp, Gpb.Colorspace.RGB, False, 8
        sizeargs = self.resize * self.width, self.resize * self.height
        pbuf = Gpb.Pixbuf.new_from_bytes(*confargs, *sizeargs, rowarg)        
        self.img.set_from_pixbuf(pbuf)

        self.tmpColor = None
        self.tmpNode = None

    def onScroll(self, box, event):
        if event.delta_y > 0:
            self.value /= 1.1
        else:
            self.value *= 1.1            
        print("value:", float(self.value))
        
    def onPress(self, widget, event):
        print("Key val: ", event.keyval)    
        print("Key name: ", Gdk.keyval_name(event.keyval))    

        if Gdk.keyval_name(event.keyval) == "r":
            printDebug(" refresh screen")
            self.refrechScreen()

        if Gdk.keyval_name(event.keyval) == "s":
            n = self.handler.diagram.smoothBorder()
            printDebug(f"smooth border: {n}")

        if Gdk.keyval_name(event.keyval) == "t":
            try:
                pattern = rgb2str(self.tmpColor)
            except TypeError: pattern = self.tmpColor
            
            for color in self.handler.diagram.terrains.keys():
                prom = "*" if color == pattern else "-" 
                terr = self.handler.diagram.terrains[color]
                printInfo(f"{prom} {color}: {terr[0]} {terr[1]} {terr[2]}")

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
                    
                
    def onExit(self, win, event):
        del(self.handler)
        Gtk.main_quit()

    def onClick(self, box, event):            
        pass
    
    def onCross(self, box, event):            
        y = int(event.y / self.resize)
        x = int(event.x / self.resize)
        x = (x + self.offset) % self.width
        # printDebug(f"click: {x} x {y}")
        
        if event.button == 1:
            if not self.tmpNode: return
            if not self.tmpColor: return
            dxy = self.handler.diagram.getStream(x,y)
            nt = self.tmpNode, rgb2str(self.tmpColor)
            self.handler.diagram[x,y] = *nt, *dxy
            try: self.handler.diagram[x+1,y] = *nt, *dxy
            except KeyError: pass
            try: self.handler.diagram[x-1,y] = *nt, *dxy
            except KeyError: pass
            try: self.handler.diagram[x,y+1] = *nt, *dxy
            except KeyError: pass
            try: self.handler.diagram[x,y-1] = *nt, *dxy
            except KeyError: pass
            
        elif event.button == 2:
            printDebug(" refresh screen")
            self.refrechScreen()
                
        elif event.button == 3:
            self.tmpNode = self.handler.diagram.getNode(x,y)
            self.tmpColor = self.handler.diagram.getColor(x,y)
            printInfo(f"node: {self.tmpNode} color: {self.tmpColor}")
            
win = DiagramViewer(sys.argv[1], 0)

try: Gtk.main()
except KeyboardInterrupt:
    print("???")
