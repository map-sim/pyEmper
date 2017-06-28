#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('GdkPixbuf', '2.0')

from gi.repository import GdkPixbuf as Gpb
from gi.repository import GLib
from gi.repository import Gtk

    
class editor(Gtk.Window):

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

        ebox = Gtk.EventBox ()
        self.fix.put(ebox, 230,0)
        ebox.connect ('button-press-event', self.on_clicked_mouse)

        self.img = Gtk.Image()
        ebox.add(self.img)
        self.refresh()

        self.button_add = Gtk.Button(label="+")
        self.button_add.connect("clicked", self.on_clicked_add)
        self.fix.put(self.button_add, 170,40)

        self.button_sub = Gtk.Button(label="-")
        self.button_sub.connect("clicked", self.on_clicked_sub)
        self.fix.put(self.button_sub, 170,75)

        combo_main = Gtk.ComboBoxText()
        self.fix.put(combo_main, 0,0)

        combo_main.connect("changed", self.on_changed_combo_main)
        issues = ["PROVINCE", "NATION", "TERRAIN", "GOOD", "CONTROL", "PROCESS"]
        for i in issues: combo_main.append_text(i)
        combo_main.set_active(0)

        combo_sub = Gtk.ComboBoxText()
        self.fix.put(combo_sub, 0, 75)

        self.name = Gtk.Entry()
        self.fix.put(self.name, 0, 40)

        self.show_all()
        
    def new_map_init(self, width, height):
        print(">> new map")
        self.width = width
        self.height = height
        self.diagram = [0, 100, 100]*self.width*self.height

    def load_map_init(self, fname):
        assert False, "Not implemented!" 

    def refresh(self):
        tmp = GLib.Bytes.new(self.diagram)        
        pbuf = Gpb.Pixbuf.new_from_bytes(tmp, Gpb.Colorspace.RGB, False, 8, self.width, self.height, 3*self.width)
        self.img.set_from_pixbuf(pbuf)
        
    def on_clicked_mouse (self, box, event):
        print(event.x, event.y)
        
    def on_changed_combo_main(self, widget):
        self.button_add.show()
        i = widget.get_active()
        
    def on_clicked_add(self, widget):
        self.button_add.hide()

    def on_clicked_sub(self, widget):
        self.button_sub.hide()


