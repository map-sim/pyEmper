#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

gi.require_version('GLib', '2.0')
from gi.repository import GLib

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf as Gpb

from globsimSQL import GlobSimSQL
from basicToolBox import printWarning
from basicToolBox import printInfo

class DiagramGTK(Gtk.Window):
    borderRGB = 0, 0, 0

    def __init__(self, database, offset=0):
        Gtk.Window.__init__(self, title="EMPER - VIEWER")
        self.connect("key-press-event",self.onPress)
        self.connect("delete-event", self.onExit)

        self.database = str(database)        
        self.handler = GlobSimSQL(database)

        self.height = self.handler.getParam("map_height")
        self.width = self.handler.getParam("map_width")
        printInfo(f"width: {self.width}")
        printInfo(f"height: {self.height}")

        project = self.handler.getParam("map_project")
        self.handler.requireMapProjection(0)
        
        self.resize = 2        
        self.value = 1.0
        self.offset = offset
        
        printInfo(f"offset: {offset}")
        printInfo(f"value: {self.value}")
        printInfo(f"resize: {self.resize}")

        fix = Gtk.Fixed()
        self.add(fix)

        ebox = Gtk.EventBox()
        fix.put(ebox, 0,0)

        ebox.connect('scroll-event', self.onScroll)
        ebox.connect ('button-press-event', self.onClick)
        ebox.add_events(Gdk.EventMask.SCROLL_MASK|Gdk.EventMask.SMOOTH_SCROLL_MASK)
        
        self.img = Gtk.Image()
        ebox.add(self.img)
                
    def extractXY(self, event):
        y = int(event.y / self.resize)
        x = int(event.x / self.resize)
        x = (x + self.offset) % self.width
        printInfo(f"click: {x} x {y}")
        return x, y
    
    def refrechScreen(self):
        diagramRGB = []
        for y in range(self.height):
            top, flo = [], []            
            for x in range(self.width):
                x = (x + self.offset) % self.width
                flag = self.checkLine(x, y)
                rgb = self.getColor(x, y)
                
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
        
    def onExit(self, win, event):
        del(self.handler)
        Gtk.main_quit()

    def onPress(self, widget, event):
        printDebug(f"Key val: {event.keyval}")    
        printDebug(f"Key name: {Gdk.keyval_name(event.keyval)}")
        
    def onScroll(self, box, event):
        if event.delta_y > 0:
            self.value /= 1.1
        else:
            self.value *= 1.1            
        printInfo(f"value: {float(self.value)}")
        
    def onClick(self, box, event):
        printWarning("onClick no implemented")
