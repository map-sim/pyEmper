#!/usr/bin/python3

class EmpTerrain:
    def __init__(self, name, rgb, con_in, con_out):
        assert len(rgb) == 3, "3 times char is excpected"
        assert con_in>=0 and con_in<=1, "con_in out of range"
        assert con_out>=0 and con_out<=1, "con_out out of range"
        assert len(name)>=3 and len(name)<=14, "too long string"
        for c in rgb: 
            assert int(c)>=0 and int(c)<256, "3 chars are excpected"
        
        self.con_out = float(con_out)
        self.con_in = float(con_in)
        self.name = str(name)
        self.rgb = tuple(rgb)

class EmpProvince:
    def __init__(self, name):
        assert len(name)>=3 and len(name)<=14, "too long string"
        self.name = str(name)

class EmpNation:
    def __init__(self, name):
        assert len(name)>=3 and len(name)<=14, "too long string"
        self.name = str(name)

class EmpCore:
    def __init__(self):
        self.nations = []
        self.terrains = []
        self.provinces = []
    
    def add_terrain(self, name, rgb, con_in, con_out):
        try: nt = EmpTerrain(name, rgb, con_in, con_out)
        except AssertionError: return -1

        for t in self.terrains:
            if name==t.name or rgb==t.rgb: return -1
        self.terrains.append(nt)
        return len(self.terrains)-1 

    def add_province(self, name):
        try: np = EmpProvince(name)
        except AssertionError: return -1

        for p in self.provinces:
            if name==p.name: return -1 
        self.provinces.append(np)
        return len(self.provinces)-1 

    def add_nation(self, name):
        try: nn = EmpNation(name)
        except AssertionError: return -1

        for n in self.nations:
            if name==n.name: return -1 
        self.nations.append(nn)
        return len(self.nations)-1 
