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

import BusyBoxSQL

class Diagram:
    def __init__(self, driver):
        assert type(driver) == BusyBoxSQL.BusyBoxSQL
        self.driver = driver
        
        project = self.driver.get_config_by_name("map_project")
        assert project == 1, "(e) not supported map projection!"

        self.width = driver.get_config_by_name("map_width")
        self.height = driver.get_config_by_name("map_height")
        ToolBox.print_output(f"original map size: {self.width} x {self.height}")

        self.set_resize(1)
        self.set_zoom(None)
        self.set_offset(0)
        self.border = False
        self.set_hopsize(50)
        assert self.refresh

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
