#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import os, sys
import sqlite3

class BasicSQL:
    def __init__(self, fname):
        if not os.path.exists(fname):
            printError(f"path {fname} not exists!")
            sys.exit(-1)

        def dict_factory(cur, row):
            gen = enumerate(cur.description)
            out = {c[0]: row[i] for i,c in gen}
            return out

        self.conn = sqlite3.connect(fname)
        self.conn.row_factory = dict_factory
        self.cur = self.conn.cursor()

    def __del__(self):
        try:
            self.conn.commit()
            self.conn.close()
        except AttributeError:
            pass
        
    def execute(self, query):        
        self.cur.execute(query)
        return self.cur.fetchall()

handler = BasicSQL("demo.sql")
gen = handler.execute("select * from config_ft")
for row in gen:
    keys, vals = [], []
    for k,v in row.items():
        keys.append(k)
        if k=="color" or k=="name":
            vals.append(f"'{v}'")
        else: vals.append(f"{v}")
    karg = ",".join(keys)
    varg = ",".join(vals) 
    cmd = f"insert into config({karg}) values ({varg})"
    handler.execute(cmd)
    print(cmd)
handler.conn.commit()
