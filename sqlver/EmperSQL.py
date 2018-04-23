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

    def __del__(self):
        print_info("database closed")
        self.conn.close()
        
    def execute(self, query):
        self.cur.execute(query)
        
    def commit(self):
        self.conn.commit()

    def select_many(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_parameter(self, name):
        query = "SELECT value FROM parameters WHERE name='%s'" % name 
        self.cur.execute(query)
        return self.cur.fetchone()[0]
