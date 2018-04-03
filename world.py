#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from terrain import EmpTerrains 
from diagram import EmpDiagram 
from nation import EmpNation
from graph import EmpGraph 

from termcolor import colored

import sqlite3
import time
import json
import os

class EmpWorld:

    def __init__(self, savedir):

        # check "/" char
        if savedir[-1] != "/": 
            savedir += "/"
            
        # load main config
        with open(savedir + "main.json") as dc:
            self.conf = json.load(dc)
            
        self.terrains = EmpTerrains(self, self.conf["terrains"])
        self.diagram = EmpDiagram(self.terrains, savedir + self.conf["diagram"])
        self.graph = EmpGraph(self.diagram, savedir + self.conf["nodes"])
            
        self.nations = {}
        for name in self.conf["nations"].keys():
            self.nations[name] = EmpNation(name, self.conf["nations"][name], self.graph)

                    
    def save(self, savedir):

        # check "/" char
        if savedir[-1] != "/": 
            savedir += "/"

        self.conf["nodes"] = "nodes.json"
        self.conf["diagram"] = "map.ppm"
        self.conf["terrains"] = self.terrains.get_conf()
        
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        else:
            warning = colored("(warning)", "yellow")
            print(warning, "dir %s exists!" % savedir)

        with open(savedir +"main.json", "w") as fd:
            json.dump(self.conf, fd)

        self.graph.save(savedir + self.conf["nodes"])
        self.diagram.save(savedir + self.conf["diagram"])
        print(colored("(info)", "red"), "save config as:", savedir)

        self.save_db("out.db")

    def save_db(self, path):

        if os.path.exists(path):
            warning = colored("(warning)", "yellow")
            print(warning, "path %s exists!" % path)
            
        conn = sqlite3.connect(path)
        cur = conn.cursor()

        query = "CREATE TABLE parameters(name text UNIQUE, value real)"
        print(query)
        cur.execute(query)
        conn.commit()

        query = "INSERT INTO parameters VALUES ('width', %d)" % self.diagram.width
        # print(query)
        cur.execute(query)

        query = "INSERT INTO parameters VALUES ('height', %d)" % self.diagram.height
        # print(query)
        cur.execute(query)

        query = "INSERT INTO parameters VALUES ('terrains', %d)" % len(self.terrains)
        # print(query)
        cur.execute(query)

        query = "INSERT INTO parameters VALUES ('nations', %d)" % len(self.nations)
        # print(query)
        cur.execute(query)

        query = "INSERT INTO parameters VALUES ('nodes', %d)" % len(self.graph)
        # print(query)
        cur.execute(query)
        conn.commit()

        
        query = "CREATE TABLE terrains(name text UNIQUE, color text UNIQUE, conduct1 real, conduct2 real, infrcost real)"
        print(query)
        cur.execute(query)
        conn.commit()
        # SELECT * FROM terrains LIMIT 1 OFFSET 5;

        for k in sorted(self.terrains.keys()):
            color = "%02X%02X%02X" % self.terrains[k].rgb
            con1 = self.terrains[k].con_base
            con2 = self.terrains[k].con_delta
            infc = self.terrains[k].infr_cost
            name = self.terrains[k].name
            
            values = "'%s', '%s', %g, %g, %g" % (name, color, con1, con2, infc)
            query = "INSERT INTO terrains VALUES (%s)" % values
            # print(query)
            cur.execute(query)
        conn.commit()


        query = "CREATE TABLE nations(name text UNIQUE, martial real, product real, fert real, loyal real, migrate real)"
        print(query)
        cur.execute(query)
        conn.commit()
        
        for n in self.nations.keys():

            values = "'%s', %g, %g, %g, %g, %g" % (n, 1, 1, 1, 1, 1)
            query = "INSERT INTO nations VALUES (%s)" % values
            # print(query)
            cur.execute(query)
        conn.commit()


        line = "name text UNIQUE"
        for n in self.nations.keys():
            line = "%s, %s real" % (line, n)
        query = "CREATE TABLE nodes(%s)" % line
        print(query)
        cur.execute(query)
        conn.commit()
         
        for n in self.graph:
            line = "'%s'" % n.name 
            for nt in self.nations.keys():
                try: pop = float(n.conf["population"][nt])
                except KeyError: pop = 0.0
                line = "%s, %f" % (line, pop)   

            query = "INSERT INTO nodes VALUES (%s)" % line
            # print(query)
            cur.execute(query)
        conn.commit()

        query = "CREATE TABLE atoms(x int, y int, node text, color text)"
        print(query)
        cur.execute(query)
        conn.commit()

        for row in self.diagram:
            for a in row:
                color = "%02X%02X%02X" % a.t.rgb                
                name = a.n.name
                       
                query = "INSERT INTO atoms VALUES (%d, %d, '%s', '%s')" % (a.x, a.y, name, color)
                # print(query)
                cur.execute(query)

        conn.commit()
        conn.close()
