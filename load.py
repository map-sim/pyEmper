#!/usr/bin/python3

import os, os.path
import sqlite3 as lite
from core import EmpCore

class EmpLoad:

    def __init__(self, fname="input.db"):
        if not os.path.isfile(fname):
            sys.stderr.write("file does not exist!")
            sys.exit(-1)

        self.con = None
        try:
            self.con = lite.connect(fname)
            self.cur = self.con.cursor()

            self.cur.execute("SELECT value FROM general_info WHERE key='width'")
            self.width = int(self.cur.fetchone()[0])

            self.cur.execute("SELECT value FROM general_info WHERE key='height'")
            self.height = int(self.cur.fetchone()[0])
            
        finally:    
            if self.con:
                self.con.close()


    def load_core(self):
        core = EmpCore(self.width, self.height)

        return core
