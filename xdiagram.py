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
parser.add_option("-E", "--edit", dest="edit",
                  action="store_true", default=False,
                  help="edit mode")
parser.add_option("-c", "--current", dest="current",
                  action="store_true", default=False,
                  help="print current instead of terrain")

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

class XDiagramGTK(Gtk.Window, Diagram.Diagram):
    def __init__(self, driver):
        Gtk.Window.__init__(self, title="xdiagram")
        Diagram.Diagram.__init__(self, driver)
        self.colorbox = self.driver.get_colors_as_list()        
        self.connect("key-press-event",self.on_press)
        self.connect("delete-event", self.on_exit)

        self.stream = []
        self.edit_mode = False
        self.current_mode = False        
        self.remembered_node = None
        self.remembered_color = None
        self.remembered_node2 = None

        self.coast_rgb = [255] * 3
        self.border_rgb = [0, 0, 0]

    def enable_edit_mode(self):
        if self.current_mode:
            raise ValueError("(e) edit mode is not supported for current map")
        self.edit_mode = True

    def enable_current_mode(self):
        if self.edit_mode:
            raise ValueError("(e) edit mode is not supported for current map")
        self.current_mode = True

    def on_exit(self, win, event):
        del(self.driver)
        Gtk.main_quit()
        
    def on_press(self, widget, event):
        ToolBox.print_output(f"Key val: {event.keyval}, ",
                             f"Key name: {Gdk.keyval_name(event.keyval)}")

        if self.shift_zoom(Gdk.keyval_name(event.keyval)): pass
        elif Gdk.keyval_name(event.keyval) == "Return":
            self.diagram = driver.get_vector_diagram()
            self.refresh()

        elif Gdk.keyval_name(event.keyval) in ["Page_Up", "Page_Down"]:
            di = 1 if Gdk.keyval_name(event.keyval) == "Page_Up" else -1
            try:
                i = self.colorbox.index(self.remembered_color)
                i = (i + di) % len(self.colorbox)
            except ValueError: i = 0

            self.remembered_color = self.colorbox[i]
            ToolBox.print_output(self.colorbox[i])
            
        elif Gdk.keyval_name(event.keyval) == "space":
            db_name = self.driver.db_name
            strstr = "-".join(self.stream)
            os.system(f"./node.py -f {db_name} -s {strstr}")

    def on_click(self, box, event):
        xo, y = Diagram.Diagram.on_click(self, box, event)
        color = self.diagram[xo,y][0]
        node = self.diagram[xo,y][1]

        if event.button == 1:
            self.remembered_color = color
            self.remembered_node = node
            self.remembered_node2 = None
            self.stream.append(node)
            ToolBox.print_output(f"{xo}x{y} = {node} / {color}")
            
        elif event.button == 2:
            if self.edit_mode and self.remembered_node and self.remembered_color:
                ToolBox.print_output(f"{node} / {color} --> {self.remembered_node} / {self.remembered_color}")
                self.driver.set_color_by_coordinates(xo, y, self.remembered_color)
                self.driver.set_node_by_coordinates(xo, y, self.remembered_node)

        elif event.button == 3 and self.remembered_node2 != node:
            db_name = self.driver.db_name
            os.system(f"./node.py -f {db_name} -n {node}")

            if self.remembered_node2 is not None:
                # self.diagram = driver.get_vector_diagram()
                cost = self.diagram.calc_transit_resistance(self.remembered_node, self.remembered_node2, node)
                ToolBox.print_output(f"{self.remembered_node} --> {self.remembered_node2} --> {node} = {cost}")
                # self.refresh()
                
            elif self.remembered_node is not None:
                # self.diagram = driver.get_vector_diagram()
                cost = self.diagram.calc_enter_resistance(self.remembered_node, node)
                ToolBox.print_output(f"{self.remembered_node} --> {node} = {cost}")
                # self.refresh()
            
            self.remembered_node2 = node
            self.stream = []

    def refresh(self):
        diagramRGB = []
        for xo, y, rows, bset in self.sceen_duoator(diagramRGB):
            rgbt = self.diagram.calc_color(xo, y, self.current_mode)
            self.pixel_painter(rgbt, rows, bset)
        self.draw_map(diagramRGB)

###
### main
###

import BusyBoxSQL
driver = BusyBoxSQL.BusyBoxSQL(opts.dbfile)
xdiagram = XDiagramGTK(driver)

zoom = {"west": int(opts.west)}
zoom["north"] = int(opts.north)
zoom["south"] = int(opts.south)
zoom["east"] = int(opts.east)
xdiagram.set_zoom(zoom)

if opts.border:
    xdiagram.set_border()
xdiagram.set_resize(opts.resize)
xdiagram.set_offset(opts.offset)
xdiagram.set_hopsize(opts.delta)

if opts.current: xdiagram.enable_current_mode()
if opts.edit: xdiagram.enable_edit_mode()

xdiagram.refresh()

try: Gtk.main()
except KeyboardInterrupt:
    ToolBox.print_error("break by keyboard")
