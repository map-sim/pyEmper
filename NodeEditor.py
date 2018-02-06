#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


import sys, os
import random
import string    
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

from world import EmpWorld 
from node import EmpNode 

SCALE = 2
RGB1 = (255, 255, 255)
RGB2 = (64, 64, 64)
RGB3 = (200, 200, 200)

def xy_gen(w, h=None):
    if not h is None:
        for y in range(h):
            for sy in range(SCALE):
                for x in range(w):
                    for sx in range(SCALE):                    
                        yield x,y
    elif isinstance(w, (set, list, tuple, EmpNode)):
        for a in w:
            for sy in range(SCALE):
                for sx in range(SCALE):                    
                    yield SCALE*a.x+sx, SCALE*a.y+sy
                    
class NodeEditor(Gtk.Window):
    def __init__(self, savefile):
        Gtk.Window.__init__(self, title="EMPER - Node Editor")
        
        self.connect('key_press_event', self.on_press_keyboard)
        fix = Gtk.Fixed()
        self.add(fix)
        
        ebox = Gtk.EventBox()
        ebox.connect ('button-press-event', self.on_clicked_mouse)
        fix.put(ebox, 0,0)
        
        self.img = Gtk.Image()
        ebox.add(self.img)
        
        self.world = EmpWorld(sys.argv[1])

        self.selected_nodes = []
        self.selected_node = None
        self.rgbmap = self.get_terrain_map()
        self.draw_borders()
        
        self.refresh(self.rgbmap)
        self.show_all()

    def refresh(self, diagram):
        colorf = Gpb.Colorspace.RGB
        tmp = GLib.Bytes.new(diagram)
        w = SCALE * self.world.diagram.width 
        h = SCALE * self.world.diagram.height
        pbuf = Gpb.Pixbuf.new_from_bytes(tmp, colorf, False, 8, w, h, 3*w)
        self.img.set_from_pixbuf(pbuf)

    def draw_borders(self):                        
        for y in range(self.world.diagram.height-1):
            for x in range(self.world.diagram.width-1):
                a = self.world.diagram[x][y]
                
                if self.world.diagram[x+1][y].n != a.n:
                    self.set_xy(SCALE*x+1, SCALE*y, RGB1)
                    self.set_xy(SCALE*(x+1), SCALE*y, RGB1)
                    self.set_xy(SCALE*x+1, SCALE*y+1, RGB1)
                    self.set_xy(SCALE*(x+1), SCALE*y+1, RGB1)
                if self.world.diagram[x][y+1].n != a.n:
                    self.set_xy(SCALE*x, SCALE*y+1, RGB1)
                    self.set_xy(SCALE*x, SCALE*(y+1), RGB1)
                    self.set_xy(SCALE*x+1, SCALE*y+1, RGB1)
                    self.set_xy(SCALE*x+1, SCALE*(y+1), RGB1)

    def set_xy(self, x, y, rgb):
        index = 3 * (x + y * SCALE * self.world.diagram.width)
        if tuple(self.rgbmap[index:index+3]) != RGB1:
            self.rgbmap[index:index+3] = rgb
        
    def get_terrain_map(self):
        g = xy_gen(self.world.diagram.width, self.world.diagram.height)
        out  = [c for x, y in g for c in self.world.diagram[x][y].t.rgb]
        return out

    def select_node(self, node):
        if node is self.selected_node:
            return
        
        g = xy_gen(self.selected_node)
        for x, y in g:
            rgb = self.world.diagram[int(x/SCALE)][int(y/SCALE)].t.rgb
            self.set_xy(x, y, rgb)

        self.selected_node = node
        g = xy_gen(node)
        for x, y in g:
            if int(x/(2*SCALE)) % 2 ^ int(y/(2*SCALE)) % 2:
                rgb = RGB2
            else: rgb = RGB3
            self.set_xy(x, y, rgb)
    
    def on_clicked_mouse (self, box, event):
        # info = "x = %.2f y = %.2f b = %d" % (event.x, event.y, event.button)
        # print(info)

        x = int(event.x/SCALE)
        y = int(event.y/SCALE)
        node = self.world.diagram[x][y].n
        print(node.name, len(node))

        if event.button == 1:
            self.select_node(node)
            self.refresh(self.rgbmap)
            self.selected_nodes.append(node)

        elif event.button == 2:
            if self.selected_node is None:
                return

            c = self.world.network.get_enter_cost(self.selected_nodes, node, 0)
            names = [n.name for n in self.selected_nodes]
            print(names, "-->", node.name, "= %.2f" % c)

        elif event.button == 3:
            if self.selected_node is None:
                return

            start = [self.selected_node]
            c = self.world.network.get_enter_cost(start, node, 0)
            print(self.selected_node.name, "-->", node.name, "= %.2f" % c)
            
    def on_press_keyboard(self, widget, event):
        print(event.keyval)

        if event.keyval == ord("p"):
            names = [n.name for n in self.selected_nodes]
            print(names)
        elif event.keyval == ord("c"):
            self.selected_nodes = []

        elif event.keyval == ord("r"):
            route = 0
            for n, node in enumerate(self.selected_nodes):
                if n>0 and n<len(self.selected_nodes)-1:
                    p = self.selected_nodes[n-1]
                    n = self.selected_nodes[n+1]
                    r = self.world.network.get_proxy_cost(p, node, n)
                    print(p.name, "-->", node.name, "-->", n.name, "= %.2f" % r)
                    route += r
            print("route = %.2f" % route)
        
if len(sys.argv) < 2:
    print("ERROR! Give a map file!")
    raise ValueError

win = NodeEditor(sys.argv[1])                
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
