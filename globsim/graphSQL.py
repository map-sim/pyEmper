#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import os, sys
import sqlite3

from basicSQL import BasicSQL
from diagramSQL import DiagramSQL

import basicToolBox
basicToolBox.debug = False
from basicToolBox import printDebug
from basicToolBox import printError

class GraphSQL(BasicSQL, dict):
    def __init__(self, fname, table="nation_sm"):
        BasicSQL.__init__(self, fname)
        dict.__init__(self)

        self.change_table(table)
        self.diagram = DiagramSQL

    def change_table(self, table):
        if not self.check_existence(table):
            printError(f"{table} not exists!")
            sys.exit(-1)
        self.table = table

    def __getitem__(self, keys):
        node, column = keys
        test = f"node='{node}'"
        rows = self.select(self.table, column, test)        
        return float(rows[0][column])

    def __setitem__(self, keys, val):
        node, column = keys
        test = f"node='{node}'"
        content = f"{column}={float(val)}"
        self.update(self.table, content, test)

