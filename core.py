#!/usr/bin/python3

from tools import  call_error

from diagram import  EmpAtom
from diagram import  EmpDiagram

class EmpIder:
    def __init__(self, core, name, tab):
        self.core = core
        self.table = tab
        
        assert len(name)>=3 and len(name)<=16, "too long string"
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
    def __repr__(self): return "p%d:%s" % (self.get_my_id(), self.name)
    def __init__(self, core, name):
        super().__init__(core, name, core.provinces)        
            
class EmpNation(EmpIder):
    def __repr__(self): return "n%d:%s" % (self.get_my_id(), self.name)
    def __init__(self, core, name):
        super().__init__(core, name, core.nations)        

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
        nt.core = self

        for t in self.terrains:
            if name==t.name: None
        self.terrains.append(nt)
        return nt 

    def rm_province(self, n):
        for i,a in enumerate(self.diagram.atoms):
            if a and a.province.get_my_id() == n:
                self.diagram.atoms[i] = None
        del self.provinces[n]
    def add_province(self, name):
        try: np = EmpProvince(self, name)
        except AssertionError: return None
        np.core = self

        for p in self.provinces:
            if name==p.name: return None
        self.provinces.append(np)
        return np
    
    def rm_nation(self, n):
        del self.nations[n]
    def add_nation(self, name):
        try: nn = EmpNation(self, name)
        except AssertionError: return None
        nn.core = self
        
        for n in self.nations:
            if name==n.name: return None
        self.nations.append(nn)
        return nn
    
    def rm_control(self, n):
        del self.controls[n]
    def add_control(self, name):
        try: nc = EmpControl(self, name)
        except AssertionError: return None
        nc.core = self

        for c in self.controls:
            if name==c.name: return None
        self.controls.append(nc)
        return nc
    
    def rm_good(self, n):        
        del self.goods[n]
    def add_good(self, name):
        try: ng = EmpGood(self, name)
        except AssertionError: return None
        ng.core = self

        for g in self.goods:
            if name==g.name: return None
        self.goods.append(ng)
        return ng
    
    def rm_process(self, n):
        del self.processes[n]
    def add_process(self, name):
        try: ns = EmpProcess(self, name)
        except AssertionError: return None
        ns.core = self

        for p in self.processes:
            if name==p.name: return None
        self.processes.append(ns)
        return ns
    
        
