#!/usr/bin/python3

import sqlite3 as lite
import os, os.path
import core, sys
import datetime

class EmpSave():

    def __init__(self, arg, fname="output.db", author="anonymous"):
        if type(arg) != type(core.EmpCore(10, 10)):
            sys.stderr.write("arg has wrong type!")
            sys.exit(-1)
        else: self.core = arg

        if os.path.isfile(fname):
            os.remove(fname)
        
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
        for p in self.core.processes:
            self.cur.execute("INSERT INTO processes VALUES('%s')" % p.name)
        self.con.commit()

