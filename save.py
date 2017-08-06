#!/usr/bin/python3

import sqlite3 as lite
import os, os.path
import core, sys
import datetime
from tools import call_error

from gi.repository import GdkPixbuf as Gpb
from gi.repository import GLib

class EmpSave():

    def __init__(self, arg, fname="save.db", author="anonymous"):
        call_error(type(arg) != type(core.EmpCore(10, 10)), "arg has wrong type!")
        if os.path.isfile(fname): os.remove(fname)

        self.core = arg        
        self.con = None
        try:
            self.con = lite.connect(fname)
            self.cur = self.con.cursor()

            print("save general info...")
            self.__save_general_info(str(author))
            print("save terrains...")
            self.__save_terrains()
            print("save provinces...")
            self.__save_provinces()
            print("save nations...")
            self.__save_nations()
            print("save controls...")
            self.__save_controls()
            print("save processes...")
            self.__save_processes()
            print("save goods...")
            self.__save_goods()

            print("save diagram...")
            self.__save_diagram()
            print("save population...")
            self.__save_population()

            print("save as", fname)
            
        finally:    
            if self.con:
                self.con.close()
        
                
    def __save_general_info(self, author):
        self.cur.execute("CREATE TABLE general_info(key TEXT, value TEXT)")
        self.cur.execute("INSERT INTO general_info VALUES('author', '%s')" % author)

        now = datetime.datetime.now()
        date_format = "%Y-%m-%d %H:%M"
        date = now.strftime(date_format)
        
        self.cur.execute("INSERT INTO general_info VALUES('date format', '%s')" % date_format)
        self.cur.execute("INSERT INTO general_info VALUES('date', '%s')" % date)
        self.cur.execute("INSERT INTO general_info VALUES('width', '%d')" % self.core.diagram.width)
        self.cur.execute("INSERT INTO general_info VALUES('height', '%d')" % self.core.diagram.height)
        self.con.commit()

    def __save_provinces(self):
        self.cur.execute("CREATE TABLE provinces(name TEXT)")
        for p in self.core.provinces:
            self.cur.execute("INSERT INTO provinces VALUES('%s')" % p.name)
        self.con.commit()

    def __save_population(self):
        self.cur.execute("CREATE TABLE population(province_name TEXT, nation_name TEXT, people INTEGER)")
        for p in self.core.provinces:
            for n in self.core.nations:
                if p.population[n] == 0: continue
                self.cur.execute("INSERT INTO population VALUES('%s', '%s', %d)" % (p.name, n.name, p.population[n]))
        self.con.commit()
        
    def __save_terrains(self):
        self.cur.execute("CREATE TABLE terrains(name TEXT, r INT,  g INT,  b INT, con REAL, ship REAL)")
        for t in self.core.terrains:
            self.cur.execute("INSERT INTO terrains VALUES('%s', %d, %d, %d, %g, %g)" % (t.name, *t.rgb, t.con, t.ship))
        self.con.commit()

    def __save_nations(self):
        self.cur.execute("CREATE TABLE nations(name TEXT)")
        for n in self.core.nations:
            self.cur.execute("INSERT INTO nations VALUES('%s')" % n.name)
        self.con.commit()

    def __save_controls(self):
        self.cur.execute("CREATE TABLE controls(name TEXT)")
        for c in self.core.controls:
            self.cur.execute("INSERT INTO controls VALUES('%s')" % c.name)
        self.con.commit()

    def __save_goods(self):
        self.cur.execute("CREATE TABLE goods(name TEXT)")
        for g in self.core.controls:
            self.cur.execute("INSERT INTO goods VALUES('%s')" % g.name)
        self.con.commit()

    def __save_processes(self):
        self.cur.execute("CREATE TABLE processes(name TEXT)")
        for x in self.core.processes:
            self.cur.execute("INSERT INTO processes VALUES('%s')" % x.name)
        self.con.commit()

    def __save_diagram(self):
        self.cur.execute("CREATE TABLE diagram(t INTEGER, p INTEGER)")
        g = ( self.core.diagram.get_atom(x, y)  for y in range(self.core.diagram.height) for x in range(self.core.diagram.width))

        for a in g:
            try: self.cur.execute("INSERT INTO diagram VALUES(%d, %d)" % (a.terrain.get_my_id(), a.province.get_my_id()))
            except: self.cur.execute("INSERT INTO diagram VALUES(%d, %d)" % (-1, -1))
        self.con.commit()

    def export_screen_to_pngfile(self, diagram_rgb, fname):
        tmp = GLib.Bytes.new(diagram_rgb)        
        pbuf = Gpb.Pixbuf.new_from_bytes(tmp, Gpb.Colorspace.RGB, False, 8, self.core.diagram.width, self.core.diagram.height, 3*self.core.diagram.width)
        pbuf.savev(fname, "png", [], [])

    def expotr_to_html(self, fname):
        with open(fname, "w") as fd:
            fd.write("<b>TERRAINS</b><br>\n")
            for t in self.core.terrains:                
                fd.write("%1.2f %1.2f " % (t.con, t.ship))
                fd.write("<canvas width='10' height='10' style='border:1px solid #000000; background: #%02x%02x%02x'></canvas>" % t.rgb)
                fd.write(" %s<br>\n" % t.name)

            fd.write("<br><b>PROVINCES</b><br>\n")
            for p in self.core.provinces:
                area, ground = p.get_area()
                fd.write("%s | %d = %d + %d<br>\n" % (p.name, area, ground, area-ground))
