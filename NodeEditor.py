#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


import sys, os
import random
import json
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('GdkPixbuf', '2.0')

from gi.repository import Gdk
from gi.repository import GdkPixbuf as Gpb
from gi.repository import GLib
from gi.repository import Gtk

from ppm import PPMloader 


class NodeEditor(Gtk.Window):
    def __init__(self, fname_map, fname_json=None):
        Gtk.Window.__init__(self, title="EMPER - Node Editor")
        
        self.connect('key_press_event', self.on_press_keyboard)
        fix = Gtk.Fixed()
        self.add(fix)
        
        ebox = Gtk.EventBox()
        ebox.connect ('button-press-event', self.on_clicked_mouse)
        fix.put(ebox, 0,0)
        
        self.img = Gtk.Image()
        ebox.add(self.img)

        self.diagram_rgb = self.get_map(fname_map)
        self.backup_rgb = self.get_map(fname_map)
        
        self.power = 1.0
        self.base = 0.1
                
        self.new_node()
        self.rgb = self.random_color()

        if fname_json:
            with open(fname_json) as dc:
                self.nodes = json.load(dc)
        else: self.nodes = []
        
        for node in self.nodes:
            for p in node["skeleton"]: 
                self.put_pixel(p[0], p[1], self.rgb)
            self.rgb = self.random_color()
            
        self.refresh()
        self.show_all()


    def get_map(self, fname):
        diagram_rgb = []
        self.width, self.height, generator = PPMloader(fname)
        for n, rgb in generator:
            rgb = [int(0.333*c) for c in rgb]
            diagram_rgb.extend(rgb)
            
        total = self.width * self.height
        if n + 1 != total:
            raise ValueError("file %s looks crashed (px = %d)" % (fname, n + 1))
        
        return diagram_rgb

    def get_pixel(self, x, y):
        rgb = []
        for n in range(3):
            i = n + 3*self.width * y + 3 * x
            rgb.append(self.backup_rgb[i])
        return rgb
    
    def new_node(self):
        if hasattr(self, "node"):
            if self.node["skeleton"]:
                self.nodes.append(self.node)
        self.node = {"skeleton": []}
                
    def put_pixel(self, x, y, rgb):
        for n, c in enumerate(rgb):
            index = n + 3*self.width * y + 3 * x
            self.diagram_rgb[index] = c
            
    def random_color(self):
        domain = [(0,0,1), (0,1,0), (1,0,0), (0,1,1), (1,0,1), (1,1,0)]
        rgbflags = random.choice(domain)
        
        out = []
        for b in rgbflags:
            if b: v = random.randint(200, 255)
            else: v = 0
            out.append(v)

        if hasattr(self, "rgbflags"):
            if self.rgbflags == rgbflags:
                return self.random_color()
            else: self.rgbflags = rgbflags
        else: self.rgbflags = rgbflags

        print(self.rgbflags)
        return out

    def refresh(self):
        tmp = GLib.Bytes.new(self.diagram_rgb)        
        pbuf = Gpb.Pixbuf.new_from_bytes(tmp, Gpb.Colorspace.RGB, False, 8, self.width, self.height, 3*self.width)
        self.img.set_from_pixbuf(pbuf)

    def clean_point(self, x, y):
        for p in self.node["skeleton"]:
            if (p[0], p[1]) == (x, y): 
                rgb = self.get_pixel(x, y)
                self.put_pixel(x, y, rgb)
                self.node["skeleton"].remove(p)
                self.refresh()
                break
                
    def clean_points(self):
        for n in self.node["skeleton"]:
            rgb = self.get_pixel(n[0], n[1])
            self.put_pixel(n[0], n[1], rgb)
        self.node["skeleton"] = []
        self.refresh()

    def checkout_points(self, x, y):            
        for node in self.nodes:
            found = False
            for p in node["skeleton"]: 
                if (p[0], p[1]) == (x, y): 
                    found = True
                    break
                
            if found:
                self.clean_points()
                self.node = node
                self.nodes.remove(node)
                break
        
    def on_clicked_mouse (self, box, event):
        print(event.x, event.y, event.button)
        
        if event.button == 1:
            self.put_pixel(int(event.x), int(event.y), self.rgb)
            point = (int(event.x), int(event.y), self.power)
            self.node["skeleton"].append(point)            
            self.refresh()
            
        elif event.button == 2:
            point = (int(event.x), int(event.y))
            self.checkout_points(*point)            

        elif event.button == 3:
            point = (int(event.x), int(event.y))
            self.clean_point(*point)
            
    def on_press_keyboard(self, widget, event):        
        if event.keyval == 32:
            print("SPACE (refresh)")
            self.refresh()
            
        elif event.keyval == ord("n"):
            print("n (next)")
            self.new_node()
            self.rgb = self.random_color()
            
        elif event.keyval == ord("0"):
            print("0 (reset)")
            self.power = 1.0
            self.base = 0.1
            
        elif event.keyval == ord("+"):
            print("+ (plus)")
            self.power += self.base
            
        elif event.keyval == ord("-"):
            print("- (minus)")
            if self.power < self.base:
                self.base /= 10
            self.power -= self.base
            
        elif event.keyval == ord("/"):
            print("/ (div)")
            self.base /= 10
            
        elif event.keyval == ord("*"):
            print("* (multi)")
            self.base *= 10
            
        elif event.keyval == ord("p"):
            print("p (print)")
            print(self.nodes)
            print(self.node)
            print("power:", self.power)
            print("base:", self.base)
            
        elif event.keyval == ord("c"):
            print("c (clear)")
            self.clean_points()

        elif event.keyval == ord("s"):
            print("s (save)")
            with open("nodes.json", "w") as fd:
                json.dump(self.nodes, fd)

if len(sys.argv) < 2:
    print("ERROR! Give a map file!")
elif len(sys.argv) < 3:
    win = NodeEditor(sys.argv[1])
else:
    win = NodeEditor(sys.argv[1], sys.argv[2])
                
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
