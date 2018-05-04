#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


class NodeDictFactory:
    
    def get_nation_distribution(self, name):
        query = "SELECT name FROM nations"
        self.cur.execute(query)
        nations = self.cur.fetchall()

        maxnat = 0
        for n in nations:
            query = "SELECT name,n_%s FROM nodes WHERE n_%s>0" % (n[0], n[0])
            nodenat = self.select_many(query)
            
            if n[0] == name:
                output = dict(nodenat)                
            for p in nodenat:                
                if maxnat < p[1]:
                    maxnat =  p[1]
        return output, maxnat

