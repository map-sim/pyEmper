#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


class EmpNode(set):
    
    def __init__(self, name, conf):
        set.__init__(self)
        
        self.name = str(name)
        self.conf = conf

        if not "population" in self.conf.keys():
            self.conf["population"] = {}

    def list_population(self):
        for k in self.conf["population"].keys():
            print("", k, self.conf["population"][k])
        
    def get_population(self):
        return sum([v for v in self.conf["population"].values()])
    
    def get_density(self):
        return self.get_population() / len(self)
    
    def get_config(self):
        return self.conf

