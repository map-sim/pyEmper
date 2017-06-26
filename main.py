#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



class MyWindow(Gtk.Window):

    def multiconstructor(init):
        def magic(self, *args):
            if len(args)==2: self.new_map_init(*map(int, args))
            elif len(args)==1: self.load_map_init(str(args[0]))
            else: assert False, "Wrong arguments number!"                 
            init(self)
        return magic

    @multiconstructor
    def __init__(self, *args):

        Gtk.Window.__init__(self, title="pg-editor")
        self.connect("delete-event", Gtk.main_quit)

        self.fix = Gtk.Fixed()
        self.add(self.fix)

        self.button = Gtk.Button(label="+")
        self.button.connect("clicked", self.on_clicked_add)
        self.fix.put(self.button, 150,0)

        combo = Gtk.ComboBoxText()
        self.fix.put(combo, 0,0)

        combo.connect("changed", self.on_changed_combo)
        issues = ["PROVINCE", "NATION", "TERRAIN", "GOOD", "CONTROL", "PROCESS"]
        for i in issues: combo.append_text(i)
        combo.set_active(0)


        self.show_all()

    def new_map_init(self, width, height):
        print(">> new map")

    def load_map_init(self, fname):
        assert False, "Not implemented!" 

    def on_changed_combo(self, widget):
        self.button.show()

        i = widget.get_active()
        print("Hello World", i)

    def on_clicked_add(self, widget):
        self.button.hide()
        print("Hello World")



import sys
if len(sys.argv) == 0:
    print ("new empty map")


#win = MyWindow()
win = MyWindow(1, 1)
# win = MyWindow("hej")

Gtk.main()
