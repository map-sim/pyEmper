#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from time import time
start_time = time() 

import sys, os
import sqlite3
import getopt
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('GdkPixbuf', '2.0')

from gi.repository import Gdk
from gi.repository import GdkPixbuf as Gpb
from gi.repository import GLib
from gi.repository import Gtk

from tools import print_out
from tools import print_info
from tools import print_error
from tools import str_to_rgb
from tools import xy_gener

from EmperSQL import EmperSQL

class TMAP_Viewer(Gtk.Window):
    def __init__(self, database, border=0.5, resize=1):
        Gtk.Window.__init__(self, title="EMPER - TMAP VIEWER")

        self.resize = int(resize)
        self.database = str(database)
        
        self.handler = EmperSQL(database)

        fix = Gtk.Fixed()
        self.add(fix)
        
        ebox = Gtk.EventBox()
        ebox.connect ('button-press-event', self.on_clicked_mouse)
        fix.put(ebox, 0,0)
        
        self.img = Gtk.Image()
        ebox.add(self.img)

        diagram = [c for color in self.handler.tmappoints_generator(border, resize) for c in color]
        height = resize * int(self.handler.get_parameter("height"))
        width = resize * int(self.handler.get_parameter("width"))
        
        tmp = GLib.Bytes.new(diagram)
        pbuf = Gpb.Pixbuf.new_from_bytes(tmp, Gpb.Colorspace.RGB, False, 8, width, height, 3*width)
        self.img.set_from_pixbuf(pbuf)        
        self.show_all()


    def on_clicked_mouse (self, box, event):

        x = int(event.x / self.resize)
        y = int(event.y / self.resize)
        name = self.handler.diagram[(x,y)][0]
        
        if event.button == 1:
            pnum = self.handler.calc_points(name)
            print_out("nodename: %s (%d)" % (name, pnum))
        elif event.button == 3:
            os.system("python3 print_node.py %s %s" % (self.database, name))
        else:
            print_out("xy coordinates: %d %d" % (x, y))

if not len(sys.argv) in (2, 3, 4):
    rest = "<database> --border=<float> --resize=<int>"
    print_error("USAGE: %s %s" % (sys.argv[0], rest))
    raise ValueError("wrong args number")

map_resize = 1
border_brightness = 1.0
longopts = ["border=", "resize="]
opts, args = getopt.getopt(sys.argv[2:], "", longopts)
for opt,arg in opts:
    if opt == "--border":
        border_brightness = float(arg)
        print_info("print borders: %g" % border_brightness)
    if opt == "--resize":
        map_resize = int(arg)
        print_info("resize map: %d" % map_resize)

win = TMAP_Viewer(sys.argv[1], border_brightness, map_resize)              
win.connect("delete-event", Gtk.main_quit)
win.show_all()

stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
try:
    Gtk.main()
except KeyboardInterrupt:
    print("???")
