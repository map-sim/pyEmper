#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from tools import *


class NodeDictFactory:
    
    def get_nation_distribution(self, name):
        query = "SELECT name FROM nations"
        self.cur.execute(query)

        maxnat = 0
        for n in self.cur.fetchall():
            query = "SELECT name,%s FROM population WHERE %s>0" % (n[0], n[0])
            nodenat = self.select_many(query)
            
            if n[0] == name:
                output = dict(nodenat)                
            for p in nodenat:                
                if maxnat < p[1]:
                    maxnat = p[1]
                    
        self.__maxgroup = maxnat
        return output

    def get_nation_maxgroup(self):
        try:
            return self.__maxgroup
        except AttributeError:
            query = "SELECT name FROM nations"
            self.cur.execute(query)

            maxnat = 0
            for n in self.cur.fetchall():
                query = "SELECT name,%s FROM population WHERE %s>0" % (n[0], n[0])
                nodenat = self.select_many(query)
            for p in nodenat:                
                if maxnat < p[1]:
                    maxnat =  p[1]

            self.__maxgroup = maxnat
            return self.__maxgroup
        
    def get_source_distribution(self, name):
        query = "SELECT name,%s FROM sources WHERE %s>0" % (name, name)
        nodesrc = self.select_many(query)    
        output = dict(nodesrc)

        if len(nodesrc) == 0:
            print_error("no enough data")
            raise ValueError("no data")
        
        maxsrc = 0.0
        for n in nodesrc:                
            if maxsrc < n[1]:
                maxsrc = n[1]
                    
        return output
