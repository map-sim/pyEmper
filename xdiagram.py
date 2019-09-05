#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

###
### opt parsing
###

import optparse, os
import ToolBox

parser = optparse. OptionParser()
parser.add_option("-f", "--db-file", dest="dbfile",
                  metavar="FILE", default="demo.sql",
                  help="saved simulator state")
parser.add_option("-n", "--north", dest="north",
                  default=-ToolBox.max_coordinate,
                  help="north coordinate")
parser.add_option("-w", "--west", dest="west",
                  default=-ToolBox.max_coordinate,
                  help="west coordinate")
parser.add_option("-s", "--south", dest="south",
                  default=ToolBox.max_coordinate,
                  help="south coordinate")
parser.add_option("-e", "--east", dest="east",
                  default=ToolBox.max_coordinate,
                  help="east coordinate")
parser.add_option("-r", "--resize", dest="resize",
                  default=1, help="resize factor")
parser.add_option("-o", "--offset", dest="offset",
                  default=0, help="rotation offset")
parser.add_option("-b", "--border", dest="border",
                  action="store_true", default=False,
                  help="print border")
parser.add_option("-d", "--delta", dest="delta",
                  default=20, help="delta/hopsize")
parser.add_option("-E", "--edit", dest="edit",
                  action="store_true", default=False,
                  help="edit mode")

opts, args = parser.parse_args()
assert int(opts.east) >= int(opts.west) 
assert int(opts.south) >= int(opts.north) 
zoom = {"west": int(opts.west)}
zoom["north"] = int(opts.north)
zoom["south"] = int(opts.south)
zoom["east"] = int(opts.east)
assert int(opts.delta) > 0 

###
### main
###

import gi, re
import BusyBoxSQL

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GLib', '2.0')
from gi.repository import GLib

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf as Gpb

class XDiagramGTK(Gtk.Window):
    def __init__(self, driver, zoom=None, resize=1, offset=0, delta=20, border=False, edit=False):
        Gtk.Window.__init__(self, title="xdiagram")
        self.connect("key-press-event",self.on_press)
        self.connect("delete-event", self.on_exit)

        self.edit_mode = bool(edit)
        self.remembered_node = None
        self.remembered_color = None
        
        assert type(driver) == BusyBoxSQL.BusyBoxSQL
        self.driver = driver
        
        self.width = driver.get_config_by_name("map_width")
        self.height = driver.get_config_by_name("map_height")
        ToolBox.print_output(f"original map size: {self.width} x {self.height}")

        project = driver.get_config_by_name("map_project")
        assert project == 1, "(e) not supported map projection!"

        self.set_zoom(zoom)
        self.delta = int(delta)
        self.set_resize(resize)
        self.set_offset(offset)
        self.set_border(border)

        fix = Gtk.Fixed()
        self.add(fix)
         
        ebox = Gtk.EventBox()
        fix.put(ebox, 0,0)
         
        # ebox.connect('scroll-event', self.onScroll)
        ebox.connect ('button-press-event', self.on_click)
        ebox.add_events(Gdk.EventMask.SCROLL_MASK|Gdk.EventMask.SMOOTH_SCROLL_MASK)

        self.img = Gtk.Image()
        ebox.add(self.img)
        self.show_all()
        self.refrech()

    def set_zoom(self, zoom):
        self.zoom = {}
        self.zoom["west"] = 0
        self.zoom["north"] = 0
        self.zoom["east"] = self.width - 1
        self.zoom["south"] = self.height - 1
        
        if zoom:
            if zoom["west"] > self.zoom["west"]: self.zoom["west"] = zoom["west"]
            if zoom["east"] < self.zoom["east"]: self.zoom["east"] = zoom["east"]
            if zoom["north"] > self.zoom["north"]: self.zoom["north"] = zoom["north"]
            if zoom["south"] < self.zoom["south"]: self.zoom["south"] = zoom["south"]

        self.zoom_width = self.zoom["east"] - self.zoom["west"] + 1
        self.zoom_height = self.zoom["south"] - self.zoom["north"] + 1
        ToolBox.print_output(f"map size: {self.zoom_width} x {self.zoom_height}")
                
    def set_resize(self, resize):
        ToolBox.print_output(f"resize: {resize}")
        assert int(resize) >= 1, "(e) resize"
        self.resize = int(resize)

    def set_offset(self, offset):
        ToolBox.print_output(f"offset: {offset}")
        self.offset = int(offset)
        
    def set_border(self, border):
        ToolBox.print_output(f"border: {border}")
        self.border = bool(border)

    def on_exit(self, win, event):
        del(self.driver)
        Gtk.main_quit()
        
    def on_press(self, widget, event):
        ToolBox.print_output(f"Key val: {event.keyval}, ",
                             f"Key name: {Gdk.keyval_name(event.keyval)}")

        if Gdk.keyval_name(event.keyval) == "Left":
            self.set_offset(self.offset - self.delta)
            self.refrech()

        elif Gdk.keyval_name(event.keyval) == "Right":
            self.set_offset(self.offset + self.delta)
            self.refrech()

        elif Gdk.keyval_name(event.keyval) == "Down":
            zoom = dict(self.zoom)
            if zoom["south"] + self.delta >= self.height:
                zoom["north"] = self.height - self.zoom_height
                zoom["south"] = self.height - 1
            else:
                zoom["south"] += self.delta
                zoom["north"] += self.delta
            self.set_zoom(zoom)
            self.refrech()

        elif Gdk.keyval_name(event.keyval) == "Up":
            zoom = dict(self.zoom)
            if zoom["north"] - self.delta < 0:
                zoom["south"] = self.zoom_height - 1
                zoom["north"] = 0
            else:
                zoom["south"] -= self.delta
                zoom["north"] -= self.delta
            self.set_zoom(zoom)
            self.refrech()

    def on_click(self, box, event):
        yc = int(event.y / self.resize)
        y = yc + self.zoom["north"]

        xc = int(event.x / self.resize)
        x = xc + self.zoom["west"]
        xo = (x + self.offset) % self.width
        color = self.diagram[xo,y][0]
        node = self.diagram[xo,y][1]

        if event.button == 1:
            ToolBox.print_output(f"{xc}x{yc} -> {xo}x{y} = {node} / {color}")
            self.remembered_color = color
            self.remembered_node = node

        elif event.button == 2:
            if self.edit_mode and self.remembered_node and self.remembered_color:
                ToolBox.print_output(f"{node} / {color} --> {self.remembered_node} / {self.remembered_color}")
                self.driver.set_color_by_coordinates(xo, y, self.remembered_color)
                self.driver.set_node_by_coordinates(xo, y, self.remembered_node)

        elif event.button == 3:
            db_name = self.driver.db_name
            os.system(f"./node.py -f {db_name} -n {node}")
            
    def refrech(self):
        self.diagram = driver.get_diagram_as_dict()

        diagramRGB = []
        borderRGB = [0, 0, 0]
        for y in range(self.zoom["north"], self.zoom["south"]+1):
            rows = [[] for _ in range(self.resize)]

            for x in range(self.zoom["west"], self.zoom["east"]+1):
                xo = (x + self.offset) % self.width
                rgb = self.diagram[xo, y][0]
                rgbt = [
                    int(rgb[2*n:2*n+2], 16)
                    for n in range(3)]

                borderset = set()
                if self.border:
                    try:
                        if self.diagram[xo, y][1] != self.diagram[xo, y+1][1]: borderset.add("S")
                    except KeyError: pass
                    try:
                        if self.diagram[xo, y][1] != self.diagram[xo, y-1][1]: borderset.add("N")
                    except KeyError: pass
                    try:
                        xoo = (xo+1) % self.width
                        if self.diagram[xo, y][1] != self.diagram[xoo, y][1]: borderset.add("W")
                    except KeyError: pass
                    try:
                        xoo = (xo-1) % self.width
                        if self.diagram[xo, y][1] != self.diagram[xoo, y][1]: borderset.add("E")
                    except KeyError: pass

                for j, row in enumerate(rows):
                    for i in range(self.resize):
                        pen = rgbt

                        if "W" in borderset and i == self.resize-1: pen = borderRGB
                        elif "S" in borderset and j == self.resize-1: pen = borderRGB
                        elif "E" in borderset and i == 0: pen = borderRGB
                        elif "N" in borderset and j == 0: pen = borderRGB
                        
                        row.extend(pen)
            for row in rows:
                diagramRGB.extend(row)

        tmp = GLib.Bytes.new(diagramRGB)
        confargs = tmp, Gpb.Colorspace.RGB, False, 8
        sizeargs = self.zoom_width * self.resize, self.zoom_height * self.resize        
        pbuf = Gpb.Pixbuf.new_from_bytes(*confargs, *sizeargs, 3 * self.zoom_width * self.resize)        
        self.img.set_from_pixbuf(pbuf)

###
### main
###

import BusyBoxSQL
driver = BusyBoxSQL.BusyBoxSQL(opts.dbfile)
xdiagram = XDiagramGTK(driver, zoom, opts.resize, opts.offset, opts.delta, opts.border, opts.edit)

try: Gtk.main()
except KeyboardInterrupt:
    ToolBox.print_error("break by keyboard")
