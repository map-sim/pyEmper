#!/usr/bin/python3

import sqlite3 as lite
import core, sys

class EmpSave(arg, fname="save.db", author="anonymous"):

    def __init__(self):
        if type(arg) != type(core.EmpCore()):
            sys.stderr.write("arg has wrong type!")
            sys.exit(-1)
        else:
            self.core = arg

        con = None
        try:
            con = lite.connect('test.db')
    
            self.cur = con.cursor()    
            cur.execute('SELECT SQLITE_VERSION()')
 
            data = self.cur.fetchone()    
            print("SQLite version: %s" % data)                
            
            self.__save_general_info()

        except lite.Error, e:
            sys.stderr.write("error: %s" % e.args[0])
            sys.exit(-1)
    
        finally:    
            if con: con.close()


    def __save_general_info(self):
        "CREATE TABLE"
    

# save(core.EmpCore())
