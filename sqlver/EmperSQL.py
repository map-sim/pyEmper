#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

import sys, os
import sqlite3

from tools import print_info
from tools import print_error

class EmperSQL:

    def __init__(self, fname):
        
        if not os.path.exists(fname):
            print_error("path %s not exists!" % fname)
            raise ValueError("database not exists")

        self.conn = sqlite3.connect(fname)
        print_info("database: %s" % fname)
        self.cur = self.conn.cursor()

        self.diagram = {}
        
    def __del__(self):
        print_info("database closed")
        self.conn.commit()
        self.conn.close()
        
    def execute(self, query):
        self.cur.execute(query)
        
    def commit(self):
        self.conn.commit()

    def enable_diagram(self):
        self.diagram = {}
        query = "SELECT x,y,node FROM atoms"
        for x,y,n in self.select_many(query):
            self.diagram[(x,y)] = n

    def is_border(self, x, y):
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            try:
                if self.diagram[(x,y)] != self.diagram[(x+dx,y+dy)]:
                    return True
            except KeyError: pass
        return False
        
    def select_many(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_parameter(self, name):
        query = "SELECT value FROM parameters WHERE name='%s'" % name 
        self.cur.execute(query)
        return self.cur.fetchone()[0]
