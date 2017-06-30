#!/usr/bin/python3

import sqlite3 as lite
import core, sys
import datetime

class EmpSave():

    def __init__(self, arg, fname="output.db", author="anonymous"):
        if type(arg) != type(core.EmpCore()):
            sys.stderr.write("arg has wrong type!")
            sys.exit(-1)
        else: self.core = arg

        self.con = None
        try:
            self.con = lite.connect(fname)
            self.cur = self.con.cursor()
                        
            self.__save_general_info(str(author))

        except lite.Error:
            sys.stderr.write("error: %s" % e.args[0])
            sys.exit(-1)
    
        finally:    
            if self.con:
                self.con.close()


    def __save_general_info(self, author):
        self.cur.execute("CREATE TABLE general_info(key TEXT, value TEXT)")
        self.cur.execute("INSERT INTO general_info VALUES('author', '%s')" % author)

        now = datetime.datetime.now()
        date_format = "%Y-%m-%d %H:%M"
        date = now.strftime(date_format)
        
        self.cur.execute("INSERT INTO general_info VALUES('date format', '%s')" % date_format)
        self.cur.execute("INSERT INTO general_info VALUES('date', '%s')" % date)
        self.con.commit()
        
s = EmpSave(core.EmpCore())
