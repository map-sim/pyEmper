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

opts, args = parser.parse_args()
assert int(opts.east) >= int(opts.west) 
assert int(opts.south) >= int(opts.north) 
zoom = {"west": int(opts.west)}
zoom["north"] = int(opts.north)
zoom["south"] = int(opts.south)
zoom["east"] = int(opts.east)

###
### main
###

import gi, re
import BasicSQL

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GLib', '2.0')
from gi.repository import GLib

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf as Gpb

class XDiagramGTK(Gtk.Window):
    def __init__(self, driver, zoom=None, resize=1, offset=0, border=False):
        assert type(driver) == BasicSQL.BasicSQL
        self.driver = driver
        
        Gtk.Window.__init__(self, title="xdiagram")
        self.width = driver.get_config_by_name("map_width")
        self.height = driver.get_config_by_name("map_height")
        ToolBox.print_output(f"original map size: {self.width} x {self.height}")

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
        
        self.connect("key-press-event",self.onPress)
        self.connect("delete-event", self.onExit)

        project = driver.get_config_by_name("map_project")
        assert project == 1, "(e) not supported map projection!"
        
        self.set_resize(resize)
        self.set_offset(offset)
        self.set_border(border)

        fix = Gtk.Fixed()
        self.add(fix)
         
        ebox = Gtk.EventBox()
        fix.put(ebox, 0,0)
         
        # ebox.connect('scroll-event', self.onScroll)
        ebox.connect ('button-press-event', self.onClick)
        ebox.add_events(Gdk.EventMask.SCROLL_MASK|Gdk.EventMask.SMOOTH_SCROLL_MASK)

        self.diagram = driver.get_diagram_as_dict()
   
        self.img = Gtk.Image()
        ebox.add(self.img)
        self.show_all()
        self.refrech()

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

    def onExit(self, win, event):
        del(self.driver)
        Gtk.main_quit()
        
    def onPress(self, widget, event):
        ToolBox.print_warning(f"Key val: {event.keyval}, ",
                             f"Key name: {Gdk.keyval_name(event.keyval)}")
    def onClick(self, box, event):
        y = int(event.y / self.resize)
        x = int(event.x / self.resize)
        xo = (x + self.offset) % self.width
        node = self.diagram[xo,y][1]
        ToolBox.print_output(f"{x}({xo})x{y} - {node}")
    
    def refrech(self):
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

import BasicSQL
driver = BasicSQL.BasicSQL(opts.dbfile)
xdiagram = XDiagramGTK(driver, zoom, opts.resize, opts.offset, opts.border)

try: Gtk.main()
except KeyboardInterrupt:
    ToolBox.print_error("break by keyboard")
