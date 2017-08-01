#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('GdkPixbuf', '2.0')

from gi.repository import GdkPixbuf as Gpb
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Gdk

import sys
from tools import  call_error

from core import EmpCore
from load import EmpLoad
from rainbow import EmpRainbow
from interpreter import EmpInterpreter
    
class EmpEditor(Gtk.Window):

    def multiconstructor(init):
        def internal(self, *args):
            if len(args)==2: self.new_map_init(*map(int, args))
            elif len(args)==1: self.load_map_init(str(args[0]))
            else: call_error(True, "wrong arguments number")
            init(self)
        return internal

    def new_map_init(self, width, height): self.core = EmpCore(width, height)
    def load_map_init(self, fname): self.core = EmpLoad(fname).load_core()

    @multiconstructor
    def __init__(self, *args):
        self.width,self.height = self.core.diagram.width, self.core.diagram.height
        self.rainbow = EmpRainbow(self.width, self.height)
        self.diagram_rgb = self.core.diagram.rgb
        self.interpreter = EmpInterpreter(self)
        self.last_click = (0,0)

        # main window ################################################################
        Gtk.Window.__init__(self, title="py-emper")
        self.connect('key_press_event', self.on_press_key)
        self.connect("delete-event", self.on_quit)
        fix = Gtk.Fixed()
        self.add(fix)
        
        ebox = Gtk.EventBox()
        ebox.connect ('button-press-event', self.on_clicked_mouse)
        fix.put(ebox, 230,0)
        
        self.img = Gtk.Image()
        ebox.add(self.img)
        self.core.diagram.draw_lines()        
        self.refresh()

        # labels ################################################################
        self.labels = {}
        self.tables = {}
        self.objects = {}
        symbols = ["p", "t", "n", "c", "g", "s", "d", "r", "x"]
        for n,s in enumerate(symbols):
            self.objects[s] = None
            self.labels[s] = Gtk.Label(s+":")
            fix.put(self.labels[s], 5, 5+n*21)
        self.tables["p"] = self.core.provinces
        self.tables["t"] = self.core.terrains
        self.tables["n"] = self.core.nations
        self.tables["c"] = self.core.controls
        self.tables["s"] = self.core.processes
        self.tables["g"] = self.core.goods
        self.set_pix_buffer([])

        self.pens = ["none", "cross", "quad", "circle"]
        self.screens = ["map", "rgb"]
        self.set_screen(0)
        self.set_pen(0)
        
        self.show_all()

    def refresh(self):
        tmp = GLib.Bytes.new(self.diagram_rgb)        
        pbuf = Gpb.Pixbuf.new_from_bytes(tmp, Gpb.Colorspace.RGB, False, 8, self.width, self.height, 3*self.width)
        self.img.set_from_pixbuf(pbuf)

    def on_press_key(self, widget, event):
        self.interpreter.put(event.keyval)

    def on_quit(self, widget, event):
        cursor = Gdk.Cursor(Gdk.CursorType.DOT)
        gdk_window = self.get_root_window()
        gdk_window.set_cursor(cursor)
        Gtk.main_quit()

    def on_clicked_mouse (self, box, event):
        self.last_click = (int(event.x), int(event.y))
        x,y = self.last_click
        
        if self.pens[self.objects["d"]] == "none" or event.button==3:
            if self.screens[self.objects["r"]] != "rgb":
                if event.button==3:
                    self.set_pix_buffer(self.core.diagram.get_area(self.last_click))
                    self.set_pen(0)
                else:
                    atom = self.core.diagram.get_atom(x,y)
                    try:
                        print(atom.terrain)
                        print(atom.province)
                        self.set_object("t", atom.terrain.get_my_id())
                        self.set_object("p", atom.province.get_my_id())
                        
                        print("p area:", self.objects["p"].get_area()[0])
                        
                    except AttributeError: pass

        elif self.pens[self.objects["d"]] == "cross":
            a = [(x,y), (x+1,y), (x-1,y), (x,y+1), (x,y-1)]
            self.core.diagram.set_area(a, self.objects["p"], self.objects["t"])
            self.refresh()
            
        elif self.pens[self.objects["d"]] == "quad":
            a = [(x+a-2,y+b-2) for a in range(5) for b in range(5)]
            self.core.diagram.set_area(a, self.objects["p"], self.objects["t"])
            self.refresh()

        elif self.pens[self.objects["d"]] == "circle":
            self.core.diagram.set_circle(self.last_click, self.objects["p"], self.objects["t"])
            self.refresh()

        elif self.pens[self.objects["d"]] == "dilation":
            self.core.diagram.dilation(self.last_click, self.objects["p"], self.objects["t"])
            self.refresh()


    def set_object(self, symbol, number):
        try:
            self.objects[symbol] = self.tables[symbol][number]
            self.labels[symbol].set_text(symbol+": "+self.objects[symbol].name)
        except IndexError:
            self.labels[symbol].set_text(symbol+":")
            self.objects[symbol] = None

    def set_pen(self, n):
        self.objects["d"] = n
        label = self.pens[self.objects["d"]]
        self.labels["d"].set_text("d:"+label)

    def set_screen(self, n):
        self.objects["r"] = n
        label = self.screens[self.objects["r"]]
        self.labels["r"].set_text("r:"+label)

    def set_pix_buffer(self, pixels):
        self.objects["x"] = pixels
        self.labels["x"].set_text("x:"+str(len(pixels)))
