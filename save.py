#!/usr/bin/python3

import sqlite3 as lite
import os, os.path
import core, sys
import datetime
from tools import call_error

class EmpSave():

    def __init__(self, arg, fname="save.db", author="anonymous"):
        call_error(type(arg) != type(core.EmpCore(10, 10)), "arg has wrong type!")
        if os.path.isfile(fname): os.remove(fname)

        self.core = arg        
        self.con = None
        try:
            self.con = lite.connect(fname)
            self.cur = self.con.cursor()
                        
            self.__save_general_info(str(author))
            self.__save_terrains()
            self.__save_provinces()
            self.__save_nations()
            self.__save_controls()
            self.__save_processes()
            self.__save_goods()

            self.__save_diagram()
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

    def __save_terrains(self):
        self.cur.execute("CREATE TABLE terrains(name TEXT, r INT,  g INT,  b INT, con_in REAL, con_out REAL)")
        for t in self.core.terrains:
            self.cur.execute("INSERT INTO terrains VALUES('%s', %d, %d, %d, %g, %g)" % (t.name, *t.rgb, t.con_in, t.con_out))
        self.con.commit()

    def __save_provinces(self):
        self.cur.execute("CREATE TABLE provinces(name TEXT)")
        for p in self.core.provinces:
            self.cur.execute("INSERT INTO provinces VALUES('%s')" % p.name)
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
        self.cur.execute("CREATE TABLE diagram(x INT, y INT, t INT, p INT)")
        g = (a for a in self.core.diagram.atoms if a)
        for a in g: self.cur.execute("INSERT INTO diagram VALUES(%d, %d, %d, %d)" % (a.x, a.y, a.terrain.get_my_id(), a.province.get_my_id()))
        self.con.commit()

    def expotr_to_html(self):
        with open("save.html", "w") as fd:
            for t in self.core.terrains:                
                fd.write("%1.2f %1.2f " % (t.con_in, t.con_out))
                fd.write("<canvas width='10' height='10' style='border:1px solid #000000; background: #%02x%02x%02x'></canvas>" % t.rgb)
                fd.write(" <b>%s</b><br>\n " % t.name)
