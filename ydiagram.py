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

parser.add_option("-p", "--province", dest="province",
                  help="point nodes")
parser.add_option("-D", "--Distribution", dest="distribution",
                  help="distribution values")
parser.add_option("-C", "--Control", dest="control",
                  help="control values")
parser.add_option("-N", "--nation", dest="nation",
                  help="nation values")
parser.add_option("-P", "--population", dest="population",
                  action="store_true", default=False,
                  help="print population")

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
import random

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

        self.coast_rgb = [0] * 3
        self.border_rgb = [160] * 3

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

        if self.nvalues is None:
            db_name = self.driver.db_name
            os.system(f"./node.py -f {db_name} -p {node}")
        else:
            try: val = self.nvalues[node]
            except KeyError: val = "-"
            ToolBox.print_output(f"{xo}x{y} = {node} -> {val}")

    def assign_node_pointer(self, nodes):
        def inner(): self.node_pointer(nodes)            
        self.assigned_painter = inner
        
    def node_pointer(self, nodes):
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

    def assign_control_presenter(self, control):
        def inner(): self.control_presenter(control)            
        self.assigned_painter = inner

    def control_presenter(self, control):
        controlmap = {}
        for node in self.driver.get_node_names_as_set():
            if not self.diagram.check_land(node): continue

            controldict = self.driver.calc_control(node)
            try: self.nvalues[node] = controldict[control]
            except KeyError: self.nvalues[node] = 0

        diagramRGB = []
        for xo, y, rows, bset in self.sceen_duoator(diagramRGB):
            node = self.diagram[xo,y][1]
            try:
                nv = self.nvalues[node]
                if nv == 0:
                    rgbt = [188, 188, 188]
                else:
                    bc = int(255 * (1.0 - nv))
                    rgbt = [bc, bc, 255]                
            except KeyError:
                rgbt = [128, 128, 128]

            self.pixel_painter(rgbt, rows, bset)            
        self.screen = diagramRGB
            
    def assign_distribution_presenter(self, distribution):
        def inner(): self.distribution_presenter(distribution)            
        self.assigned_painter = inner
        
    def distribution_presenter(self, distribution):
        self.nvalues = self.driver.get_distribution_as_dict(distribution)
        diagramRGB = []
     
        maxv = self.driver.get_max_distribution(distribution)
        assert maxv > 0, "(e) no distribution"
    
        for xo, y, rows, bset in self.sceen_duoator(diagramRGB):
            node = self.diagram[xo,y][1]
            try: nv = self.nvalues[node] / maxv
            except KeyError: nv = 0.0
            bc = int(255 * (1.0 - nv))
            rgbt = [bc, bc, 255]
            self.pixel_painter(rgbt, rows, bset)            
        self.screen = diagramRGB

    def assign_nation_presenter(self, nation):
        def inner(): self.nation_presenter(nation)            
        self.assigned_painter = inner
        
    def nation_presenter(self, nation):
        self.nvalues = self.driver.get_population_as_dict(nation)
        diagramRGB = []
        
        maxv = self.driver.get_max_population(nation)
        assert maxv > 0, "(e) no population"
    
        for xo, y, rows, bset in self.sceen_duoator(diagramRGB):
            node = self.diagram[xo,y][1]
            if self.nvalues[node]:
                nv = self.nvalues[node] / maxv
                bc = int(255 * (1.0 - nv))
                gc = int(127 * (1.0 - nv))
                rgbt = [128+gc, bc, bc]
            else: rgbt = [220, 220, 220]
            self.pixel_painter(rgbt, rows, bset)            
        self.screen = diagramRGB
        
    def assign_population_presenter(self):
        def inner(): self.population_presenter()            
        self.assigned_painter = inner

    def population_presenter(self):
        self.nvalues = self.driver.get_population_as_dict()
        diagramRGB = []

        maxv = self.driver.get_max_population()
        assert maxv > 0, "(e) no population"

        for xo, y, rows, bset in self.sceen_duoator(diagramRGB):
            node = self.diagram[xo,y][1]
            if self.nvalues[node]:
                nv = self.nvalues[node] / maxv
                bc = int(255 * (1.0 - nv))
                gc = int(127 * (1.0 - nv))
                rgbt = [128+gc, 128+gc, bc]
            else: rgbt = [220, 220, 220]
            self.pixel_painter(rgbt, rows, bset)            
        self.screen = diagramRGB

    def assign_color_nation_presenter(self, cstr):
        colors = {}        
        nrgbl = cstr.split("-")
        for nrgb in nrgbl:
            n, r,g,b = nrgb.split(":")
            colors[n] = int(r), int(g), int(b)

        def inner(): self.color_nation_presenter(colors)            
        self.assigned_painter = inner

    def color_nation_presenter(self, color_nation):
        self.nvalues = None
        bgrgb = [220, 220, 220]
        diagramRGB = []
        cache = {}
        for xo, y, rows, bset in self.sceen_duoator(diagramRGB):
            node = self.diagram[xo,y][1]
            try: colors, weights = cache[node]
            except KeyError:
                popdict = self.driver.get_population_by_node_as_dict(node)
                popsum = sum([v for n,v in popdict.items() if n != "node"])
                colors, weights = [], []
                for nation, color in color_nation.items():
                    if popsum == 0: break
                    frac = float(popdict[nation]) / popsum 
                    weights.append(frac)
                    colors.append(color)
                frac = 1.0 - sum(weights)
                weights.append(frac)
                colors.append(bgrgb)
                cache[node] = colors, weights
            try: rgbt = random.choices(colors, weights)[0]
            except IndexError:  rgbt = bgrgb
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

if opts.province:
    title = "ydiagram - province"
elif opts.control:
    title = "ydiagram - control"
elif opts.population:
    title = "ydiagram - population"
elif opts.nation:
    title = f"ydiagram - nation - {opts.nation}"
elif opts.distribution:
    title = f"ydiagram - distribution - {opts.distribution}"
else: raise ValueError("(e) what")

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

if opts.province:
    nodes = opts.province.split("-")
    ydiagram.assign_node_pointer(nodes)

elif opts.population:
    if opts.nation is None:
        ydiagram.assign_population_presenter()
    else: ydiagram.assign_color_nation_presenter(opts.nation)

elif opts.nation:
    ydiagram.assign_nation_presenter(opts.nation)

elif opts.control:
    ydiagram.assign_control_presenter(opts.control)

elif opts.distribution:
    ydiagram.assign_distribution_presenter(opts.distribution)

else:
    ydiagram.assign_node_pointer("")
ydiagram.refresh()

try: Gtk.main()
except KeyboardInterrupt:
    ToolBox.print_error("break by keyboard")
