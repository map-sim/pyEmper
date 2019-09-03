#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import os, sys
import sqlite3
import ToolBox

class BasicSQL:
    __ints = ["map_width", "map_height", "map_project"]
    
    def __init__(self, fname):
        if not os.path.exists(fname):
            ToolBox.print_error(f"path {fname} not exists!")
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

    ###
    ### config specific
    ###
    
    def get_config_by_name(self, name):
        out = self.execute(f"SELECT value FROM config WHERE name='{name}'")
        assert len(out) == 1, "(e) outlen != 1"
        if name in self.__ints:
            return int(out[0]["value"])
        else: return out[0]["value"]

    def set_config_by_name(self, name, value):
        self.execute(f"UPDATE config SET value={value} WHERE name='{name}'")
        if self.cur.rowcount == 0:
            self.execute(f"INSERT INTO config(name, value) VALUES ('{name}', {value})")
        
    def delete_config_by_name(self, name):
        self.execute(f"DELETE FROM config WHERE name='{name}'")

    def get_config_as_dict(self):
        out = self.execute("SELECT * FROM config")
        assert len(out) > 0, "(e) config length < 1"

        dout = {}
        for drow in out:
            if drow['name'] in self.__ints:                
                dout[drow['name']] = int(drow['value'])
            else: dout[drow['name']] = drow['value']
        return dout

    ###
    ### diagram specific
    ###

    def get_diagram_as_dict(self):
        out = self.execute("SELECT * FROM diagram")
        assert len(out) > 0, "(e) diagram length < 1"
        ca = self.get_config_by_name("current_amplitude")
    
        dout = {}
        for drow in out:
            xykey = drow["x"], drow["y"]
            dc = drow["dx"]/ca, drow["dy"]/ca
            col = drow["color"]
            node = drow["node"]
            dout[xykey] = col, node, dc
        return dout
