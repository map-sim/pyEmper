#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import os
import sqlite3

from globsimTools import printDebug
from globsimTools import printInfo

class BasicSQL:
    def __init__(self, fname):
        if not os.path.exists(fname):
            print_error("path %s not exists!" % fname)
            raise ValueError("database not exists")

        self.conn = sqlite3.connect(fname)
        printInfo("database: %s" % fname)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.conn.close()
        printInfo("database: closed...")
        
    def commit(self):
        self.conn.commit()
        
    def execute(self, query):
        self.cur.execute(query)                
        printDebug(query)
        
    def select(self, table, content="*", test=None, extra=""):        
        if test:
            query = f"SELECT {content} FROM {table} WHERE {test}"
        else: query = f"SELECT {content} FROM {table}"
            
        self.execute(f"{query} {extra}")
        out = self.cur.fetchall()
        return out

    def update(self, table, content, test):        
        query = f"UPDATE {table} SET {content} WHERE {test}"
        self.execute(query)
        self.commit()
        
    def insert(self, table, content):        
        query = f"INSERT INTO {table} VALUES({content})"
        self.execute(query)
        self.commit()
 
