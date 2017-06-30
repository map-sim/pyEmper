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
import save
    
class EmpEditor(Gtk.Window):

    main_issues = ["TERRAIN", "PROVINCE", "NATION", "CONTROL", "GOOD", "PROCESS"]

    def multiconstructor(init):
        def internal(self, *args):
            if len(args)==2: self.new_map_init(*map(int, args))
            elif len(args)==1: self.load_map_init(str(args[0]))
            else: assert False, "Wrong arguments number!"                 
            init(self)
        return internal

    @multiconstructor
    def __init__(self, *args):
        
        # window and fixer
        Gtk.Window.__init__(self, title="gtk-editor")
        self.connect("delete-event", Gtk.main_quit)
        fix = Gtk.Fixed()
        self.add(fix)
        
        # event box for mouse clicks
        ebox = Gtk.EventBox()
        ebox.connect ('button-press-event', self.on_clicked_mouse)
        fix.put(ebox, 230,0)

        # image for map presenting
        self.img = Gtk.Image()
        ebox.add(self.img)
        self.refresh()

        # side panel - name entry
        self.name = Gtk.Entry()
        fix.put(self.name, 0, 110)
 
        # side panel - spins
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

        # list of spins
        self.spins = [self.rspin, self.gspin, self.bspin, self.ispin, self.ospin]

        # side panel - buttons
        self.abut = Gtk.Button(label="+")
        self.abut.connect("clicked", self.on_clicked_add)
        fix.put(self.abut, 170, 110)

        self.sbut = Gtk.Button(label="-")
        self.sbut.connect("clicked", self.on_clicked_sub)
        fix.put(self.sbut, 170, 75)

        self.svbut = Gtk.Button(label="SAVE")
        self.svbut.connect("clicked", self.on_clicked_save)
        fix.put(self.svbut, 0, self.height-35)

        # side panel - combos
        self.scombo = Gtk.ComboBoxText()
        self.scombo.connect("changed", self.on_changed_scombo)
        fix.put(self.scombo, 0, 70)

        self.mcombo = Gtk.ComboBoxText()
        self.mcombo.connect("changed", self.on_changed_mcombo)
        fix.put(self.mcombo, 0, 0)

        for i in self.main_issues: 
            self.mcombo.append_text(i)
        
        # endig
        self.idic = {}
        for i in self.main_issues: 
            self.idic[i] = -1 

        self.show_all()
        self.clean_panel()
        self.mcombo.set_active(0)
        self.refill_scombo()
        self.scam_mode = "input"

    def new_map_init(self, width, height):
        print(">> new map")
        self.width = width
        self.height = height
        self.diagram = [0, 100, 100]*self.width*self.height
        self.core = core.EmpCore()

    def load_map_init(self, fname):
        assert False, "Not implemented!" 

    def refill_scombo(self):
        self.scombo.remove_all()        
        nr = self.mcombo.get_active()
        if self.main_issues[nr] == "TERRAIN": [self.scombo.append_text(i.name) for i in self.core.terrains]
        elif self.main_issues[nr] == "PROVINCE": [self.scombo.append_text(i.name) for i in self.core.provinces]
        elif self.main_issues[nr] == "NATION": [self.scombo.append_text(i.name)for i in self.core.nations]
        elif self.main_issues[nr] == "CONTROL": [self.scombo.append_text(i.name)for i in self.core.controls]
        elif self.main_issues[nr] == "GOOD": [self.scombo.append_text(i.name)for i in self.core.goods]
        elif self.main_issues[nr] == "PROCESS": [self.scombo.append_text(i.name)for i in self.core.processes]
        self.scombo.set_active(self.idic[self.main_issues[nr]])                


    def refresh(self):
        tmp = GLib.Bytes.new(self.diagram)        
        pbuf = Gpb.Pixbuf.new_from_bytes(tmp, Gpb.Colorspace.RGB, False, 8, self.width, self.height, 3*self.width)
        self.img.set_from_pixbuf(pbuf)
        
    def on_clicked_mouse (self, box, event):
        print(event.x, event.y)
        
    def on_changed_mcombo(self, widget):
        self.scam_mode="output"
        self.refill_scombo()
        self.clean_panel()
        self.scam_mode="input"

    def on_changed_scombo(self, widget):
        self.clean_panel()
        if self.scam_mode=="input":
            i = widget.get_active()
            nr = self.mcombo.get_active()
            self.idic[self.main_issues[nr]] = i
        else:
            pass

    def clean_panel(self):
        self.name.hide()
        self.name.set_text("")
        for s in self.spins: s.hide()
        
    def on_clicked_save(self, widget):        
        s = save.EmpSave(self.core)
        
    def on_clicked_add(self, widget):
        nr,res = self.mcombo.get_active(),-1
        if not self.name.is_visible() :            
            if self.main_issues[nr] == "TERRAIN":
                for i in self.spins: i.show()                 
            elif self.main_issues[nr] == "PROVINCE": pass
            elif self.main_issues[nr] == "NATION": pass
            elif self.main_issues[nr] == "CONTROL": pass
            elif self.main_issues[nr] == "GOOD": pass
            elif self.main_issues[nr] == "PROCESS": pass
            self.name.show()
        else:
            if self.main_issues[nr] == "TERRAIN":
                name = self.name.get_text()
                r,g,b,i,o = [i.get_value() for i in self.spins]                
                res = self.core.add_terrain(name, (r,g,b), 0.01*i, 0.01*o)
                print("add terain (%d)" % res)

            elif self.main_issues[nr] == "PROVINCE":
                res = self.core.add_province(self.name.get_text())
                print("add province (%d)" % res)

            elif self.main_issues[nr] == "NATION":
                res = self.core.add_nation(self.name.get_text())
                print("add nation (%d)" % res)

            elif self.main_issues[nr] == "CONTROL":
                res = self.core.add_control(self.name.get_text())
                print("add control (%d)" % res)

            elif self.main_issues[nr] == "GOOD":
                res = self.core.add_good(self.name.get_text())
                print("add good (%d)" % res)

            elif self.main_issues[nr] == "PROCESS":
                res = self.core.add_process(self.name.get_text())
                print("add process (%d)" % res)

            if res >= 0:
                self.scam_mode="output"
                self.idic[self.main_issues[nr]] = res
                self.refill_scombo()
                self.scam_mode="input"
                
            self.clean_panel()
        self.abut.show()

    def on_clicked_sub(self, widget):
        self.clean_panel()


