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

from toolbox import measure_time
from toolbox import xy_gen

from world import EmpWorld 
from node import EmpNode 

SCALE = 2 # only 2 and 1
RGB1 = (255, 255, 255)
RGB2 = (64, 64, 64)
RGB3 = (200, 200, 200)


class NodeEditor(Gtk.Window):
    def __init__(self, savefile):
        Gtk.Window.__init__(self, title="EMPER - Node Editor")
        
        self.connect('key_press_event', self.on_press_keyboard)
        fix = Gtk.Fixed()
        self.add(fix)
        
        ebox = Gtk.EventBox()
        ebox.add_events(Gdk.EventMask.SCROLL_MASK|Gdk.EventMask.SMOOTH_SCROLL_MASK)
        ebox.connect ('button-press-event', self.on_clicked_mouse)
        ebox.connect('scroll-event', self.on_scrolled_mouse)
        fix.put(ebox, 0,0)
        
        self.img = Gtk.Image()
        ebox.add(self.img)
        
        self.world = EmpWorld(sys.argv[1])
        self.value = 2.0
        
        nkey = list(self.world.nations.keys())[0]
        self.selected_nation = self.world.nations[nkey]

        self.selected_nodes = []
        self.selected_node = None
        
        self.rgbmap = self.get_terrain_map()
        self.maptype = "terrain"
        
        self.draw_borders(RGB1)
        self.refresh(self.rgbmap)
        self.show_all()

    def refresh(self, diagram):
        colorf = Gpb.Colorspace.RGB
        tmp = GLib.Bytes.new(diagram)
        w = SCALE * self.world.diagram.width 
        h = SCALE * self.world.diagram.height
        pbuf = Gpb.Pixbuf.new_from_bytes(tmp, colorf, False, 8, w, h, 3*w)
        self.img.set_from_pixbuf(pbuf)

    def draw_node_borders(self, node, rgb):
        for a in node:
            if not self.world.diagram.isborder(a): continue
            if a.x == 0 or a.y == 0: continue
            if a.x == self.world.diagram.width-1: continue
            if a.y == self.world.diagram.height-1: continue
            if not self.world.diagram[a.x+1][a.y].n is a.n:
                self.set_xy(SCALE*a.x+1, SCALE*a.y, rgb)
                self.set_xy(SCALE*(a.x+1), SCALE*a.y, rgb)
                self.set_xy(SCALE*a.x+1, SCALE*a.y+1, rgb)
                self.set_xy(SCALE*(a.x+1), SCALE*a.y+1, rgb)
            if not self.world.diagram[a.x][a.y+1].n is a.n:
                self.set_xy(SCALE*a.x, SCALE*a.y+1, rgb)
                self.set_xy(SCALE*a.x, SCALE*(a.y+1), rgb)
                self.set_xy(SCALE*a.x+1, SCALE*a.y+1, rgb)
                self.set_xy(SCALE*a.x+1, SCALE*(a.y+1), rgb)

    @measure_time("border draw")
    def draw_borders(self, rgb):
        for n in self.world.graph:
            self.draw_node_borders(n, rgb)

    def set_xy(self, x, y, rgb):
        index = 3 * (x + y * SCALE * self.world.diagram.width)
        if tuple(self.rgbmap[index:index+3]) != RGB1:
            self.rgbmap[index:index+3] = rgb

    @measure_time("terrains draw")
    def get_terrain_map(self):
        g = xy_gen(SCALE, self.world.diagram.width, self.world.diagram.height)
        out  = [c for x, y in g for c in self.world.diagram[x][y].t.rgb]
        return out

    @measure_time("nations draw")
    def get_nation_map(self):
        m = self.world.graph.get_max_population()
        print("max population in nodes:", int(m))
        
        out = []
        g = xy_gen(SCALE, self.world.diagram.width, self.world.diagram.height)
        for x, y in g:
            if not self.world.diagram[x][y].t.isground():
                out.extend([0, 128, 255])
            elif self.world.diagram[x][y].t.isriver():
                out.extend([255, 32, 32])
            else:
                try: v = self.world.diagram[x][y].n.conf["population"][self.selected_nation.name]
                except KeyError: v = 0
                if v == 0:
                    out.extend([160, 160, 160])
                else:
                    c = int(255 * (1.0 - float(v) / m))
                    out.extend([0, c, 0])
        return out

    @measure_time("density draw")
    def get_density_map(self):
        m = self.world.graph.get_max_density()
        print("max density in nodes:", m)

        out = []
        g = xy_gen(SCALE, self.world.diagram.width, self.world.diagram.height)
        for x, y in g:
            if not self.world.diagram[x][y].t.isground():
                out.extend([0, 128, 255])
            elif self.world.diagram[x][y].t.isriver():
                out.extend([255, 32, 32])
            else:
                try: v = self.world.diagram[x][y].n.get_density()
                except KeyError: v = 0
                if v == 0:
                    out.extend([160, 160, 160])
                else:
                    c = int(255 * (1.0 - float(v) / m))
                    out.extend([0, c, 0])
        return out
        
    def select_node(self, node):
        if node is self.selected_node:
            return
        
        if self.maptype == "terrain":
            g = xy_gen(SCALE, self.selected_node)
            for x, y in g:
                rgb = self.world.diagram[int(x/SCALE)][int(y/SCALE)].t.rgb
                self.set_xy(x, y, rgb)

        self.selected_node = node
        
        if self.maptype == "terrain":
            g = xy_gen(SCALE, node)
            for x, y in g:
                self.set_xy(x, y, RGB2 if int(x/(2*SCALE)) % 2 ^ int(y/(2*SCALE)) % 2 else RGB3)
    
    def on_clicked_mouse (self, box, event):
        # info = "x = %.2f y = %.2f b = %d" % (event.x, event.y, event.button)
        # print(info)

        x = int(event.x/SCALE)
        y = int(event.y/SCALE)
        node = self.world.diagram[x][y].n
        print(node.name, "atoms:", len(node), "population: %d" % node.get_population(), "density: %.3f" % (node.get_population() / len(node)))

        if event.button == 1:
            self.select_node(node)
            self.refresh(self.rgbmap)
            self.selected_nodes.append(node)
            if self.maptype == "nation" or self.maptype == "density":
                node.list_population()

        elif event.button == 2:
            if self.selected_node is None:
                return

            c = self.world.graph.get_enter_cost(self.selected_nodes, node, 0)
            names = [n.name for n in self.selected_nodes]
            print(names, "-->", node.name, "= %.2f" % c)

        elif event.button == 3:
            if self.selected_node is None:
                return

            start = [self.selected_node]
            c = self.world.graph.get_enter_cost(start, node, 0)
            print(self.selected_node.name, "-->", node.name, "= %.2f" % c)
            
    def on_scrolled_mouse(self, box, event):
        if event.delta_y > 0:
            self.value /= 1.2
        else:
            self.value *= 1.8
        if self.selected_node:
            print("value: %.3f %.3f" % (self.value, self.value/len(self.selected_node)))
        else:
            print("value: %.3f" % self.value)
        
    def on_press_keyboard(self, widget, event):
        # print(event.keyval)
        if event.keyval == ord("h"):
            print("help: hpdr012mnN")

        elif event.keyval == ord("0"):
            self.rgbmap = self.get_terrain_map()
            self.maptype = "terrain"
            self.draw_borders(RGB1)
            self.refresh(self.rgbmap)

        elif event.keyval == ord("1"):
            self.rgbmap = self.get_density_map()
            self.maptype = "density"            
            self.draw_borders(RGB1)
            self.refresh(self.rgbmap)
            
        elif event.keyval == ord("2"):
            self.rgbmap = self.get_nation_map()
            self.maptype = "nation"            
            self.draw_borders(RGB1)
            self.refresh(self.rgbmap)

        elif event.keyval == ord(" "):
            self.value = 2.0
            print("value: %.3f" % self.value)
            
        if event.keyval == ord("p"):
            names = [n.name for n in self.selected_nodes]
            print(names)
        elif event.keyval == ord("d"):
            self.selected_nodes = []

        elif event.keyval == ord("r"):
            route = 0
            if len(self.selected_nodes) > 1:
                c = self.world.graph.get_enter_cost([self.selected_nodes[1]], self.selected_nodes[0])
                print(self.selected_nodes[0].name, ">-", self.selected_nodes[1].name, "= %.2f" % c)
                route += c

            for n, node in enumerate(self.selected_nodes):                    
                if n>0 and n<len(self.selected_nodes)-1:
                    p = self.selected_nodes[n-1]
                    n = self.selected_nodes[n+1]
                    r = self.world.graph.get_proxy_cost(p, node, n)
                    print(p.name, "--", node.name, "--", n.name, "= %.2f" % r)
                    route += r

            if len(self.selected_nodes) > 1:
                c = self.world.graph.get_enter_cost([self.selected_nodes[-2]], self.selected_nodes[-1])
                print(self.selected_nodes[-2].name, "-<", self.selected_nodes[-1].name, "= %.2f" % c)
                route += c

            print("route = %.2f" % route)
            
        elif event.keyval == ord("s"):
            self.world.save("output.save")
            
        elif event.keyval == ord("m"):
            name = self.maptype
            if self.maptype == "nation":
                name += "-" + str(self.selected_nation.name)
            name += ".png"
            self.img.get_pixbuf().savev(name, "png", "", "")
            print("save:", name)
            
        # change printed nation
        elif event.keyval == ord("n"):
            nkeys = list(self.world.nations.keys())
            n = nkeys.index(self.selected_nation.name)
            n = (n+1) % len(nkeys)
            self.selected_nation = self.world.nations[nkeys[n]]
            
            if self.selected_node is None:
                p = self.selected_nation.get_population()
                print(self.selected_nation.name, int(p))
                return

            try: p = self.selected_node.conf["population"][self.selected_nation.name]
            except KeyError: p = 0
            print(self.selected_nation.name, int(p))

        # write nation
        elif event.keyval == ord("N"):
            if self.selected_node is None: return
            val = 0 if self.value < 2 else self.value
            self.selected_node.conf["population"][self.selected_nation.name] = val
            nname = self.selected_nation.name 
            print(nname, int(self.selected_node.conf["population"][nname]))

            
if len(sys.argv) < 2:
    print("ERROR! Give a map file!")
    raise ValueError

win = NodeEditor(sys.argv[1])                
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
