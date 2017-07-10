#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('GdkPixbuf', '2.0')

from gi.repository import GdkPixbuf as Gpb
from gi.repository import GLib
from gi.repository import Gtk

import sys
from core import EmpCore
from save import EmpSave
from load import EmpLoad
from rainbow import EmpRainbow
from tools import  call_error
    
class EmpEditor(Gtk.Window):

    def multiconstructor(init):
        def internal(self, *args):
            if len(args)==2: self.new_map_init(*map(int, args))
            elif len(args)==1: self.load_map_init(str(args[0]))
            else: call_error(True, "wrong arguments number")
            init(self)
        return internal

    main_issues = ["TERRAIN", "PROVINCE", "NATION", "CONTROL", "GOOD", "PROCESS"]

    def new_map_init(self, width, height): self.core = EmpCore(width, height)
    def load_map_init(self, fname): self.core = EmpLoad(fname).load_core()

    @multiconstructor
    def __init__(self, *args):

        # set section ################################################################
        self.idic = dict((i, -1) for i in self.main_issues)
        self.width,self.height = self.core.diagram.width, self.core.diagram.height
        self.diagram_rgb = self.core.diagram.rgb
        self.screen_mode = "topo-map"
        self.scam_mode = "input"
        
        self.rainbow = EmpRainbow(self.width, self.height)
        self.last_click = (0,0)

        # window and main panel ################################################################
        Gtk.Window.__init__(self, title="py-emper")
        self.connect("delete-event", Gtk.main_quit)
        fix = Gtk.Fixed()
        self.add(fix)
        
        ebox = Gtk.EventBox()
        ebox.connect ('button-press-event', self.on_clicked_mouse)
        fix.put(ebox, 230,0)
        
        self.img = Gtk.Image()
        ebox.add(self.img)
        self.refresh()

        # side panel ################################################################
        self.name = Gtk.Entry()
        fix.put(self.name, 61, 82)
 
        # side panel - spins ################################################################
        self.ispin = Gtk.SpinButton()
        adj = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self.ispin.set_adjustment(adj)
        fix.put(self.ispin, 0, 119)

        self.ospin = Gtk.SpinButton()
        adj = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self.ospin.set_adjustment(adj)
        fix.put(self.ospin, 115, 119)

        self.spins = [self.ispin, self.ospin]

        # side panel - buttons ################################################################
        self.abut = Gtk.Button(label="+")
        self.abut.connect("clicked", self.on_clicked_add)
        fix.put(self.abut, 0, 82)

        self.sbut = Gtk.Button(label="-")
        self.sbut.connect("clicked", self.on_clicked_sub)
        fix.put(self.sbut, 179, 45)

        self.svbut = Gtk.Button(label="SAVE")
        self.svbut.connect("clicked", self.on_clicked_save)
        fix.put(self.svbut, 160, self.height-35)

        # side panel - combos ################################################################
        self.scombo = Gtk.ComboBoxText()
        fix.put(self.scombo, 0, 45)

        self.mcombo = Gtk.ComboBoxText()
        fix.put(self.mcombo, 0, 0)
        for i in self.main_issues: self.mcombo.append_text(i)

        self.dcombo = Gtk.ComboBoxText()
        fix.put(self.dcombo, 0, self.height-35)
        for i in ["cross", "square", "circle", "border"]:
            self.dcombo.append_text(i)

        self.mcombo.set_active(0)
        self.refill_scombo()

        self.mcombo.connect("changed", self.on_changed_mcombo)
        self.scombo.connect("changed", self.on_changed_scombo)
        self.dcombo.connect("changed", self.on_changed_dcombo)
                
        # endig ################################################################   
        self.show_all()
        self.clean_panel()        

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
        self.core.diagram.draw_lines()
        tmp = GLib.Bytes.new(self.diagram_rgb)        
        pbuf = Gpb.Pixbuf.new_from_bytes(tmp, Gpb.Colorspace.RGB, False, 8, self.width, self.height, 3*self.width)
        self.img.set_from_pixbuf(pbuf)
        
    def on_clicked_mouse (self, box, event):
        self.last_click = (int(event.x), int(event.y))
        print("click", *self.last_click)
        if self.screen_mode == "topo-map" and self.idic["TERRAIN"]!=-1 and self.idic["PROVINCE"]!=-1:
            nr = self.dcombo.get_active()
            x,y = self.last_click
            if nr==0:
                a = [(x,y), (x+1,y), (x-1,y), (x,y+1), (x,y-1)]
                self.core.diagram.set_area(a, self.idic["PROVINCE"], self.idic["TERRAIN"])
            elif nr==1:
                a = [(x+a-2,y+b-2) for a in range(5) for b in range(5)]
                self.core.diagram.set_area(a, self.idic["PROVINCE"], self.idic["TERRAIN"])
            elif nr==2: self.core.diagram.set_circle(self.last_click, self.idic["PROVINCE"], self.idic["TERRAIN"])
            elif nr==3: self.core.diagram.set_border(self.last_click, self.idic["PROVINCE"], self.idic["TERRAIN"])
            self.refresh()
        
    def on_changed_mcombo(self, widget):
        self.scam_mode="output"
        self.refill_scombo()
        self.clean_panel()
        self.scam_mode="input"
        
    def on_changed_scombo(self, widget):
        self.clean_panel()
        if self.scam_mode=="input":
            i = self.scombo.get_active()
            nr = self.mcombo.get_active()
            self.idic[self.main_issues[nr]] = i
            if self.main_issues[nr] == "TERRAIN": print(self.core.terrains[i])
            elif self.main_issues[nr] == "PROVINCE": print(self.core.provinces[i])
            elif self.main_issues[nr] == "NATION": print(self.core.nations[i])
            elif self.main_issues[nr] == "CONTROL": print(self.core.controls[i])
            elif self.main_issues[nr] == "PROCESS": print(self.core.processes[i])
            elif self.main_issues[nr] == "GOOD": print(self.core.goods[i])
        else: pass

    def on_changed_dcombo(self, widget):
        self.core.diagram.refresh()
        self.refresh()

        
    def clean_panel(self):
        self.name.hide()
        self.name.set_text("")
        for s in self.spins: s.hide()
        if self.screen_mode == "rainbow":
            self.screen_mode = "topo-map"
            self.diagram_rgb = self.core.diagram.rgb
            self.refresh()
        
    def on_clicked_save(self, widget):
        print("save as save.db")
        s = EmpSave(self.core)
        s.expotr_to_html()
        
    def on_clicked_add(self, widget):
        nr,res = self.mcombo.get_active(),-1
        if not self.name.is_visible() :            
            if self.main_issues[nr] == "TERRAIN":
                for i in self.spins: i.show()
                self.diagram_rgb = self.rainbow.rgb
                self.screen_mode = "rainbow"
                self.refresh()

            elif self.main_issues[nr] == "PROVINCE": pass
            elif self.main_issues[nr] == "NATION": pass
            elif self.main_issues[nr] == "CONTROL": pass
            elif self.main_issues[nr] == "GOOD": pass
            elif self.main_issues[nr] == "PROCESS": pass
            self.name.show()
        else:
            if self.main_issues[nr] == "TERRAIN":
                name = self.name.get_text()
                i,o = [i.get_value() for i in self.spins]                
                r,g,b = self.rainbow.get_rgb_color(*self.last_click)

                scombo_index = self.scombo.get_active()
                if not name and scombo_index>=0:
                    self.core.terrains[scombo_index].set_parameters((r,g,b), 0.01*i, 0.01*o)
                    print("mod", str(self.core.terrains[scombo_index]))
                else:
                    res = self.core.add_terrain(name, (r,g,b), 0.01*i, 0.01*o)
                    if res>=0: print("add", str(self.core.terrains[res]))
                    else: print("cannot add terain")
                        
            elif self.main_issues[nr] == "PROVINCE":
                res = self.core.add_province(self.name.get_text())
                if res>=0: print("add", str(self.core.provinces[res]))
                else: print("cannot add province")

            elif self.main_issues[nr] == "NATION":
                res = self.core.add_nation(self.name.get_text())
                if res>=0: print("add", str(self.core.nations[res]))
                else: print("cannot add nation")

            elif self.main_issues[nr] == "CONTROL":
                res = self.core.add_control(self.name.get_text())
                if res>=0: print("add", str(self.core.controls[res]))
                else: print("cannot add control")

            elif self.main_issues[nr] == "GOOD":
                res = self.core.add_good(self.name.get_text())
                if res>=0: print("add", str(self.core.goods[res]))
                else: print("cannot add good")

            elif self.main_issues[nr] == "PROCESS":
                res = self.core.add_process(self.name.get_text())
                if res>=0: print("add", str(self.core.processes[res]))
                else: print("cannot add process")

            if res >= 0:
                self.scam_mode="output"
                self.idic[self.main_issues[nr]] = res
                self.refill_scombo()
                self.scam_mode="input"

            self.clean_panel()
        self.abut.show()

    def on_clicked_sub(self, widget):
        scombo_index = self.scombo.get_active()
        if scombo_index==-1: return

        res, nr = True, self.mcombo.get_active()
        if self.main_issues[nr] == "TERRAIN": res = self.core.rm_terrain(scombo_index)
        elif self.main_issues[nr] == "PROVINCE": res = self.core.rm_province(scombo_index)
        elif self.main_issues[nr] == "NATION": res = self.core.rm_nation(scombo_index)
        elif self.main_issues[nr] == "CONTROL": res = self.core.rm_control(scombo_index)
        elif self.main_issues[nr] == "GOOD": res = self.core.rm_good(scombo_index)
        elif self.main_issues[nr] == "PROCESS": res = self.core.rm_process(scombo_index)
        
        if res: return
        self.scam_mode="output"
        if self.core.terrains:
            self.idic[self.main_issues[nr]] = 0
        else: self.idic[self.main_issues[nr]] = -1
        self.refill_scombo()
        self.scam_mode="input"
        self.clean_panel()
