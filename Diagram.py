#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

###
### opt parsing
###

import ToolBox
def add_parser_options(parser):
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
    parser.add_option("-d", "--delta", dest="delta",
                  default=50, help="delta/hopsize")
    parser.add_option("-b", "--border", dest="border",
                      action="store_true", default=False,
                      help="print border")

###
### Diagram definition
###

import gi
import BusyBoxSQL

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

gi.require_version('GLib', '2.0')
from gi.repository import GLib

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf as Gpb

class Diagram:
    def __init__(self, driver):
        assert type(driver) == BusyBoxSQL.BusyBoxSQL
        self.driver = driver
        
        project = self.driver.get_config_by_name("map_project")
        assert project == 1, "(e) not supported map projection!"

        self.width = driver.get_config_by_name("map_width")
        self.height = driver.get_config_by_name("map_height")
        ToolBox.print_output(f"original map size: {self.width} x {self.height}")
        self.diagram = self.driver.get_vector_diagram()

        self.set_resize(1)
        self.set_zoom(None)
        self.set_offset(0)
        self.border = False
        self.set_hopsize(50)
        assert self.refresh
    
        fix = Gtk.Fixed()
        self.add(fix)
         
        ebox = Gtk.EventBox()
        fix.put(ebox, 0,0)
         
        # ebox.connect('scroll-event', self.on_scroll)
        ebox.connect ('button-press-event', self.on_click)
        ebox.add_events(Gdk.EventMask.SCROLL_MASK|Gdk.EventMask.SMOOTH_SCROLL_MASK)

        self.img = Gtk.Image()
        ebox.add(self.img)
        self.show_all()

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
                
    def set_hopsize(self, delta):
        ToolBox.print_output(f"hopsize: {delta}")
        assert int(delta) >= 1, "(e) delta/hopsize"
        self.delta = int(delta)

    def set_resize(self, resize):
        ToolBox.print_output(f"resize: {resize}")
        assert int(resize) >= 1, "(e) resize"
        self.resize = int(resize)

    def set_offset(self, offset):
        ToolBox.print_output(f"offset: {offset}")
        self.offset = int(offset)
        
    def set_border(self):
        ToolBox.print_output("border: True")
        self.border = True

    def shift_zoom(self, keyname):
        if keyname == "Left":
            self.set_offset(self.offset - self.delta)
            self.refresh()
            return True
        
        elif keyname == "Right":
            self.set_offset(self.offset + self.delta)
            self.refresh()
            return True

        elif keyname == "Down":
            zoom = dict(self.zoom)
            if zoom["south"] + self.delta >= self.height:
                zoom["north"] = self.height - self.zoom_height
                zoom["south"] = self.height - 1
            else:
                zoom["south"] += self.delta
                zoom["north"] += self.delta
            self.set_zoom(zoom)
            self.refresh()
            return True

        elif keyname == "Up":
            zoom = dict(self.zoom)
            if zoom["north"] - self.delta < 0:
                zoom["south"] = self.zoom_height - 1
                zoom["north"] = 0
            else:
                zoom["south"] -= self.delta
                zoom["north"] -= self.delta
            self.set_zoom(zoom)
            self.refresh()
            return True
        else: return False

    def on_click(self, box, event):
        yc = int(event.y / self.resize)
        y = yc + self.zoom["north"]
        xc = int(event.x / self.resize)
        x = xc + self.zoom["west"]
        xo = (x + self.offset) % self.width
        return xo, y

    def sceen_duoator(self, diagramRGB):
        for y in range(self.zoom["north"], self.zoom["south"]+1):
            rows = [[] for _ in range(self.resize)]
            for x in range(self.zoom["west"], self.zoom["east"]+1):
                xo = (x + self.offset) % self.width
                if self.border:
                    borderset = self.diagram.check_border(xo, y)
                else: borderset = set()

                yield xo, y, rows, borderset        

            for row in rows:
                diagramRGB.extend(row)
                
    def pixel_painter(self, rgbt, rows, bset):
        for j, row in enumerate(rows):
            for i in range(self.resize):
                pen = rgbt
                if "W" in bset and i == self.resize-1:
                    if "w" in bset: pen = self.coast_rgb
                    else: pen = self.border_rgb
                elif "S" in bset and j == self.resize-1:
                    if "s" in bset: pen = self.coast_rgb
                    else: pen = self.border_rgb
                elif "E" in bset and i == 0:
                    if "e" in bset: pen = self.coast_rgb
                    else: pen = self.border_rgb
                elif "N" in bset and j == 0:
                    if "n" in bset: pen = self.coast_rgb
                    else: pen = self.border_rgb                  
                row.extend(pen)

    def draw_map(self, diagramRGB):
        tmp = GLib.Bytes.new(diagramRGB)
        confargs = tmp, Gpb.Colorspace.RGB, False, 8
        sizeargs = self.zoom_width * self.resize, self.zoom_height * self.resize        
        pbuf = Gpb.Pixbuf.new_from_bytes(*confargs, *sizeargs, 3 * self.zoom_width * self.resize)        
        self.img.set_from_pixbuf(pbuf)
