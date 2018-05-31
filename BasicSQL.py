#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

import os
import sqlite3
from tools import *


class BasicSQL:
    def __init__(self, fname):
        if not os.path.exists(fname):
            print_error("path %s not exists!" % fname)
            raise ValueError("database not exists")

        self.conn = sqlite3.connect(fname)
        print_info("database: %s" % fname)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.conn.close()
        print_info("database closed")
        
    def commit(self):
        self.conn.commit()
        
    def execute(self, query):
        self.cur.execute(query)
        
    def select_many(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def select_row(self, query, number=0):
        self.cur.execute("%s LIMIT 1 OFFSET %d" % (query, number))
        return self.cur.fetchone()

    def get_table_columns(self, table):
        query = "PRAGMA table_info('%s')" % table
        self.cur.execute(query)
        info = self.cur.fetchall()
        names = [i[1] for i in info]
        return names
