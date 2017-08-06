#!/usr/bin/python3

from tools import  call_error

from diagram import  EmpAtom
from diagram import  EmpDiagram

class EmpIder:
    def __init__(self, core, name, tab):
        self.core = core
        self.table = tab
        self.set_name(name)
        self.table.append(self)

    def set_name(self, name):
        assert len(name)>=3 and len(name)<=16, "too long string"
        for obj in self.table: assert name!=obj.name
        self.name = str(name)
        
    def get_my_id(self):
        for i,t in enumerate(self.table):
            if t.name == self.name: return i
        return -1

class EmpTerrain(EmpIder):
    def __repr__(self):
        k = self.get_my_id(), self.name, self.con, self.ship, *self.rgb
        return "t%d:%s %g %g (%d,%d,%d)" % k

    def __init__(self, core, name, rgb, con, ship):
        super().__init__(core, name, core.terrains)        
        self.set_ship(ship)
        self.set_con(con)
        self.set_rgb(rgb)

    def set_con(self, con):
        assert con>=0 and con<=1, "con out of range"
        self.con = float(con)

    def set_ship(self, ship):
        assert ship>=0 and ship<=1, "ship out of range"
        self.ship = float(ship)
        
    def set_rgb(self, rgb):
        assert len(rgb) == 3, "3 times char is excpected"
        for c in rgb: assert int(c)>=0 and int(c)<256, "3 chars are excpected"
        self.rgb = tuple(rgb)
            
class EmpProvince(EmpIder):
    def __repr__(self):
        out = "p%d:%s" % (self.get_my_id(), self.name)
        out += "\n   area: %d (%d)" % self.get_area()
        for k in self.population.keys():
            if self.population[k]>0: out += "\n   pop %s: %d" % (k.name, self.population[k])
        return out
    
    def __init__(self, core, name):
        super().__init__(core, name, core.provinces)

        self.population = {}
        for n in self.core.nations:
            self.population[n] = 0
        
    def get_area(self):
        area,ground = 0,0
        g = (a for a in self.core.diagram.atoms if a.province is self)
        for a1 in g:
            area += 1
            if a1.terrain.ship<0.5: ground += 1
        return area,ground


class EmpNation(EmpIder):
    def __repr__(self): return "n%d:%s" % (self.get_my_id(), self.name)
    def __init__(self, core, name):
        super().__init__(core, name, core.nations)        
        
        for p in self.core.provinces:
            p.population[self] = 0

class EmpControl(EmpIder):
    def __repr__(self): return "c%d:%s" % (self.get_my_id(), self.name)
    def __init__(self, core, name):
        super().__init__(core, name, core.controls)        

class EmpGood(EmpIder):
    def __repr__(self): return "g%d:%s" % (self.get_my_id(), self.name)
    def __init__(self, core, name):
        super().__init__(core, name, core.goods)        

class EmpProcess(EmpIder):
    def __repr__(self): return "x%d:%s" % (self.get_my_id(), self.name)
    def __init__(self, core, name):
        super().__init__(core, name, core.processes)        


class EmpCore:
    def __init__(self, width, height):
        call_error(width<10 or height<10, "width or height < 2")
        self.diagram = EmpDiagram(self, width, height)
        
        self.terrains = []
        self.provinces = []
        self.nations = []
        self.controls = []
        self.processes = []
        self.goods = []
        
    def rm_terrain(self, n):
        for i,a in enumerate(self.diagram.atoms):
            if a and a.terrain.get_my_id() == n:
                self.diagram.atoms[i] = None
        del self.terrains[n]
    def add_terrain(self, name, rgb, con, ship):
        try: nt = EmpTerrain(self, name, rgb, con, ship)
        except AssertionError: return None
        return nt
    
    def swap_terrains(self, n1, n2):
        if n1==n2: return
        t1 = self.terrains[n1]
        t2 = self.terrains[n2]
        self.terrains[n1] = t2
        self.terrains[n2] = t1
        

    def rm_province(self, n):
        for i,a in enumerate(self.diagram.atoms):
            if a and a.province.get_my_id() == n:
                self.diagram.atoms[i] = None
        del self.provinces[n]
    def add_province(self, name):
        try: np = EmpProvince(self, name)
        except AssertionError: return None
        return np
    def get_province_by_name(self, name):
        for p in self.provinces:
            if name == p.name: return p
            
    def rm_nation(self, n):
        del self.nations[n]
    def add_nation(self, name):
        try: nn = EmpNation(self, name)
        except AssertionError: return None
        return nn
    def get_nation_by_name(self, name):
        for n in self.nations:
            if name == n.name: return n
    
    def rm_control(self, n):
        del self.controls[n]
    def add_control(self, name):
        try: nc = EmpControl(self, name)
        except AssertionError: return None
        return nc
    
    def rm_good(self, n):        
        del self.goods[n]
    def add_good(self, name):
        try: ng = EmpGood(self, name)
        except AssertionError: return None
        return ng
    
    def rm_process(self, n):
        del self.processes[n]
    def add_process(self, name):
        try: ns = EmpProcess(self, name)
        except AssertionError: return None
        return ns
    
        
