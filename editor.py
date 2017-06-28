#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('GdkPixbuf', '2.0')

from gi.repository import GdkPixbuf as Gpb
from gi.repository import GLib
from gi.repository import Gtk

import sys
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

        #  =========================================================

        self.name = Gtk.Entry()
        fix.put(self.name, 0, 110)

        self.rspin = Gtk.SpinButton()
        adj = Gtk.Adjustment(0, 0, 255, 1, 10, 0)
        self.rspin.set_adjustment(adj)
        fix.put(self.rspin, 0, 145)

        self.gspin = Gtk.SpinButton()
        adj = Gtk.Adjustment(0, 0, 255, 1, 10, 0)
        self.gspin.set_adjustment(adj)
        fix.put(self.gspin, 0, 180)
        
        self.bspin = Gtk.SpinButton()
        adj = Gtk.Adjustment(0, 0, 255, 1, 10, 0)
        self.bspin.set_adjustment(adj)
        fix.put(self.bspin, 0, 215)

        self.ispin = Gtk.SpinButton()
        adj = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self.ispin.set_adjustment(adj)
        fix.put(self.ispin, 0, 250)

        self.ospin = Gtk.SpinButton()
        adj = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self.ospin.set_adjustment(adj)
        fix.put(self.ospin, 0, 285)

        # =============================================================

        self.abut = Gtk.Button(label="+")
        self.abut.connect("clicked", self.on_clicked_add)
        fix.put(self.abut, 170, 110)

        self.sbut = Gtk.Button(label="-")
        self.sbut.connect("clicked", self.on_clicked_sub)
        fix.put(self.sbut, 170, 75)

        self.scombo = Gtk.ComboBoxText()
        fix.put(self.scombo, 0, 70)

        self.mcombo = Gtk.ComboBoxText()
        self.mcombo.connect("changed", self.on_changed_mcombo)
        fix.put(self.mcombo, 0, 0)

        for i in self.main_issues: 
            self.mcombo.append_text(i)
        self.mcombo.set_active(0)
        self.refill_scombo()
        
        # =============================================================

        self.show_all()
        self.clean_panel()

    def refill_scombo(self):
        self.scombo.remove_all()        
        nr = self.mcombo.get_active()
        if self.main_issues[nr] == "TERRAIN":
            for i in self.core.terrains: 
                self.scombo.append_text(i.name)
        else: pass
         
    def on_enter(self, width):
        print("enter")
        
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
        
    def on_changed_mcombo(self, widget):
        self.refill_scombo()
        self.clean_panel()

    def clean_panel(self):
        self.name.set_text("")
        self.name.hide()
        self.ispin.hide()
        self.ospin.hide()
        self.rspin.hide()
        self.gspin.hide()
        self.bspin.hide()
        
    def on_clicked_add(self, widget):
        nr = self.mcombo.get_active()
        if not self.name.is_visible() :            
            if self.main_issues[nr] == "TERRAIN":
                spins = (self.rspin, self.gspin, self.bspin, self.ispin, self.ospin)
                for i in spins: i.show()                 
            self.name.show()
        else:
            if self.main_issues[nr] == "TERRAIN":
                name = self.name.get_text()
                r = self.rspin.get_value()
                g = self.gspin.get_value()
                b = self.bspin.get_value()
                i = self.ispin.get_value()
                o = self.ospin.get_value()                
                res = self.core.add_terrain(name, (r,g,b), i, o)
                print("add terain (%d)" % res)
                self.refill_scombo()
            self.clean_panel()

    def on_clicked_sub(self, widget):
        self.sbut.hide()


