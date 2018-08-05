#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


import os
import sys
import json
import getopt
from tools import *


class MapExtracter:

    long_opts = ["palette=", "resize="]
    short_opts = ["rivers", "median"]

    map_resize = 1
    rivers_flag = False
    median_flag = False
    color_scheme = None


    def parse_palette(self):
        tmplist = self.long_opts + self.short_opts
        opts, args = getopt.getopt(sys.argv[3:], "", tmplist)
        for opt,arg in opts:
            if opt == "--palette":
                if not os.path.exists(arg):
                    print_error("PALETTE does not exist: %s" % arg)
                    raise ValueError("wrong arg value")
                print_info("palette: %s" % arg)
            
                with open(arg) as f:
                    self.color_scheme = json.load(f)
                return self.color_scheme
        else:
            print_error("palette has to be loaded")
            raise ValueError("palette")
                
    def parse_resize(self):
        tmplist = self.long_opts + self.short_opts
        opts, args = getopt.getopt(sys.argv[3:], "", tmplist)
        for opt,arg in opts:
            if opt == "--resize":
                self.map_resize = int(arg)
                print_info("resize map: %d" % self.map_resize)
                break
            
        return self.map_resize

    def parse_median(self):
        tmplist = self.long_opts + self.short_opts
        opts, args = getopt.getopt(sys.argv[3:], "", tmplist)
        for opt,arg in opts:
            if opt == "--resize":
                self.median_flag = True
                print_info("medianing: on")
                break
            
        return self.median_flag

    def parse_rivers(self):
        tmplist = self.long_opts + self.short_opts
        opts, args = getopt.getopt(sys.argv[3:], "", tmplist)
        for opt,arg in opts:
            if opt == "--rivers":
                self.rivers_flag = True
                print_info("rivers: on")
                break
            
        return self.rivers_flag

