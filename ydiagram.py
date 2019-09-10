#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

###
### opt parsing
###

import optparse
import ToolBox
import Diagram

parser = optparse. OptionParser()
Diagram.add_parser_options(parser)

parser.add_option("-p", "--point", dest="point",
                  help="point nodes")
parser.add_option("-S", "--source", dest="source",
                  help="source values")

opts, args = parser.parse_args()
assert int(opts.east) >= int(opts.west) 
assert int(opts.south) >= int(opts.north) 
assert int(opts.resize) > 0 
assert int(opts.delta) > 0 

###
### window definition
###

import gi, os
import BusyBoxSQL

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class YDiagramGTK(Gtk.Window, Diagram.Diagram):
    def __init__(self, driver, title):
        Gtk.Window.__init__(self, title=title)
        Diagram.Diagram.__init__(self, driver)

        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.connect("key-press-event",self.on_press)
        self.connect("delete-event", self.on_exit)
        self.nvalues = {}
        
    def on_exit(self, win, event):
        del(self.driver)
        Gtk.main_quit()
        
    def on_press(self, widget, event):
        ToolBox.print_output(f"Key val: {event.keyval}, ",
                             f"Key name: {Gdk.keyval_name(event.keyval)}")

        if self.shift_zoom(Gdk.keyval_name(event.keyval)): pass
        elif Gdk.keyval_name(event.keyval) == "Return":
            self.diagram = self.driver.get_vector_diagram()
            self.refresh()

    def on_click(self, box, event):
        xo, y = Diagram.Diagram.on_click(self, box, event)
        node = self.diagram[xo,y][1]
        try: val = self.nvalues[node]
        except KeyError: val = "-"
        ToolBox.print_output(f"{xo}x{y} = {node} -> {val}")

    def assign_node_pointer(self, nodes):
        def inner(): self.node_pointer(nodes)            
        self.assigned_painter = inner
        
    def node_pointer(self, nodes):
        self.coast_rgb = [255] * 3
        self.border_rgb = [0, 0, 0]
        diagramRGB = []
        for xo, y, rows, bset in self.sceen_duoator(diagramRGB):
            node = self.diagram[xo,y][1]
            land = self.diagram.check_land(node)

            if land:
                if node in nodes: rgbt = [255, 128, 128]
                else: rgbt = [192, 192, 192]
            else:
                if node in nodes: rgbt = [128, 128, 255]
                else: rgbt = [128, 128, 128]
                                        
            self.pixel_painter(rgbt, rows, bset)
        self.screen = diagramRGB

    def assign_source_presenter(self, source):
        def inner(): self.source_presenter(source)            
        self.assigned_painter = inner
        
    def source_presenter(self, source):
        self.coast_rgb = [0] * 3
        self.border_rgb = [180] * 3
        # self.coast_rgb = [0, 0, 255]
        # self.border_rgb = [255, 0, 0]
        diagramRGB = []
        
        self.nvalues = self.driver.get_source_as_dict(source)
        maxv = self.driver.get_max_source(source)
        assert maxv > 0, "(e) no source"
    
        for xo, y, rows, bset in self.sceen_duoator(diagramRGB):
            node = self.diagram[xo,y][1]
            # land = self.diagram.check_land(node)
            nv = self.nvalues[node] / maxv
            bc = int(255 * (1.0 - nv))
            rc = int(255 * nv)
            rgbt = [bc, bc, 255]
            # diagramRGB.extend(rgbt)
            self.pixel_painter(rgbt, rows, bset)
            
        self.screen = diagramRGB
    
    def refresh(self):
        self.assigned_painter()
        self.draw_map(self.screen)
 
###
### main
###

import BusyBoxSQL
driver = BusyBoxSQL.BusyBoxSQL(opts.dbfile)

if opts.point: title = "ydiagram"
elif opts.source: title = opts.source
ydiagram = YDiagramGTK(driver, title)

zoom = {"west": int(opts.west)}
zoom["north"] = int(opts.north)
zoom["south"] = int(opts.south)
zoom["east"] = int(opts.east)
ydiagram.set_zoom(zoom)

if opts.border:
    ydiagram.set_border()
ydiagram.set_resize(opts.resize)
ydiagram.set_offset(opts.offset)
ydiagram.set_hopsize(opts.delta)

if opts.point:
    nodes = opts.point.split("-")
    ydiagram.assign_node_pointer(nodes)

elif opts.source:
    ydiagram.assign_source_presenter(opts.source)
    
else:
    ydiagram.assign_node_pointer("")
ydiagram.refresh()

try: Gtk.main()
except KeyboardInterrupt:
    ToolBox.print_error("break by keyboard")
