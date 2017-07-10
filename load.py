#!/usr/bin/python3

import sys, os, os.path
import sqlite3 as lite
from core import EmpCore
from tools import call_error

class EmpLoad:

    def __init__(self, fname="save.db"):
        call_error(not os.path.isfile(fname), "file does not exist!")

        self.con = None
        try:
            self.con = lite.connect(fname)
            self.con.row_factory = lite.Row
            self.cur = self.con.cursor()

            self.cur.execute("SELECT value FROM general_info WHERE key='width'")
            self.width = int(self.cur.fetchone()[0])

            self.cur.execute("SELECT value FROM general_info WHERE key='height'")
            self.height = int(self.cur.fetchone()[0])

            self.core = EmpCore(self.width, self.height)

            self.cur.execute("SELECT * FROM terrains")
            rows = self.cur.fetchall()
            for t in rows:
                rgb = (int(t['r']), int(t['g']), int(t['b']))
                con_in,con_out = float(t['con_in']),float(t['con_out'])
                self.core.add_terrain(t['name'], rgb, con_in, con_out)

            self.cur.execute("SELECT * FROM provinces")
            rows = self.cur.fetchall()
            for p in rows: self.core.add_province(p['name'])

            self.cur.execute("SELECT * FROM nations")
            rows = self.cur.fetchall()
            for n in rows: self.core.add_nation(n['name'])

            self.cur.execute("SELECT * FROM controls")
            rows = self.cur.fetchall()
            for c in rows: self.core.add_control(c['name'])
            
            self.cur.execute("SELECT * FROM goods")
            rows = self.cur.fetchall()
            for g in rows: self.core.add_good(g['name'])

            self.cur.execute("SELECT * FROM processes")
            rows = self.cur.fetchall()
            for x in rows: self.core.add_process(x['name'])

        finally:    
            if self.con:
                self.con.close()

    def load_core(self): return self.core
