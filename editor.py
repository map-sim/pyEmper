#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('GdkPixbuf', '2.0')

from gi.repository import GdkPixbuf as Gpb
from gi.repository import GLib
from gi.repository import Gtk

import core
    
class GtkEditor(Gtk.Window):

    main_issues = ["PROVINCE", "NATION", "TERRAIN", "GOOD", "CONTROL", "PROCESS"]

    def multiconstructor(init):
        def internal(self, *args):
            if len(args)==2: self.new_map_init(*map(int, args))
            elif len(args)==1: self.load_map_init(str(args[0]))
            else: assert False, "Wrong arguments number!"                 
            init(self)
        return internal

    @multiconstructor
    def __init__(self, *args):

        Gtk.Window.__init__(self, title="gtk-editor")
        self.connect("delete-event", Gtk.main_quit)
        fix = Gtk.Fixed()
        self.add(fix)
        
        ebox = Gtk.EventBox()
        ebox.connect ('button-press-event', self.on_clicked_mouse)
        fix.put(ebox, 230,0)

        self.img = Gtk.Image()
        ebox.add(self.img)
        self.refresh()

        self.abut = Gtk.Button(label="+")
        self.abut.connect("clicked", self.on_clicked_add)
        fix.put(self.abut, 170, 110)

        self.sbut = Gtk.Button(label="-")
        self.sbut.connect("clicked", self.on_clicked_sub)
        fix.put(self.sbut, 170, 75)

        self.mcombo = Gtk.ComboBoxText()
        # self.mcombo.connect("changed", self.on_changed_mcombo)
        fix.put(self.mcombo, 0, 0)

        for i in self.main_issues: 
            self.mcombo.append_text(i)
        self.mcombo.set_active(0)

        self.scombo = Gtk.ComboBoxText()
        fix.put(self.scombo, 0, 75)

        #  =========================================================

        self.show_all()

        self.name = Gtk.Entry()
        self.name.set_size_request(100,45)
        fix.put(self.name, 0, 110)

        self.rgb = (Gtk.Entry(), Gtk.Entry(), Gtk.Entry())
        for i,c in enumerate(self.rgb):
            c.set_size_request(245, 45)
            fix.put(c, i*45, 145+i*)


        
    def new_map_init(self, width, height):
        print(">> new map")
        self.width = width
        self.height = height
        self.diagram = [0, 100, 100]*self.width*self.height
        self.core = core.EmpCore()

    def load_map_init(self, fname):
        assert False, "Not implemented!" 

    def refresh(self):
        tmp = GLib.Bytes.new(self.diagram)        
        pbuf = Gpb.Pixbuf.new_from_bytes(tmp, Gpb.Colorspace.RGB, False, 8, self.width, self.height, 3*self.width)
        self.img.set_from_pixbuf(pbuf)
        
    def on_clicked_mouse (self, box, event):
        print(event.x, event.y)
        
    # def on_changed_mcombo(self, widget):

    def clean_edit(self):
        self.name.set_text("")
        self.name.hide()
        for c in self.rgb:
            c.set_text("")
            c.hide()

        
    def on_clicked_add(self, widget):
        n = self.mcombo.get_active()
        if not self.name.is_visible():
            self.name.show()
            if self.main_issues[n] == "TERRAIN":
                for c in self.rgb: c.show()
        else: 
            self.clean_edit();

    def on_clicked_sub(self, widget):
        self.sbut.hide()


