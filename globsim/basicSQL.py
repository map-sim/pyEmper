#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import os, sys
import sqlite3

import basicToolBox
basicToolBox.debug = False
from basicToolBox import printDebug
from basicToolBox import printError

class BasicSQL:
    direct = True
    
    def __init__(self, fname):
        if not os.path.exists(fname):
            printError(f"path {fname} not exists!")
            sys.exit(-1)

        printDebug("database: %s" % fname)
        self.conn = sqlite3.connect(fname)
        self.cur = self.conn.cursor()

    def __del__(self):
        try:
            self.conn.commit()
            self.conn.close()
            printDebug("database: closed...")
        except AttributeError:
            pass
        
    def commit(self):
        self.conn.commit()
        
    def execute(self, query):        
        self.cur.execute(query)
        printDebug(query)
        
    def select(self, table, content="*", test=None, extra=""):        
        if not (test is None):
            query = f"SELECT {content} FROM {table} WHERE {test}"
        else: query = f"SELECT {content} FROM {table}"
            
        self.execute(f"{query} {extra}")
        out = self.cur.fetchall()
        return out

    def update(self, table, content, test):        
        query = f"UPDATE {table} SET {content} WHERE {test}"
        self.execute(query)
        if self.direct:
            self.commit()
        
    def insert(self, table, content):        
        query = f"INSERT INTO {table} VALUES({content})"
        self.execute(query)
        if self.direct:
            self.commit()
 
