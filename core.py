#!/usr/bin/python3

from tools import  call_error

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


class EmpAtom:
    def __init__(self, diagram, x, y, province, terrain):
        self.province = province
        self.terrain = terrain
        self.diagram = diagram
        
        self.n = x + y*self.diagram.width
        self.x,self.y = x,y
        
    def check_border(self):        
        try:
            try:
                if not self.province is self.diagram.get_atom(self.x+1, self.y).province: return True
            except AttributeError:  return True
            try:
                if not self.province is self.diagram.get_atom(self.x-1, self.y).province: return True
            except AttributeError:  return True
            try:
                if not self.province is self.diagram.get_atom(self.x, self.y+1).province: return True
            except AttributeError:  return True
            try:
                if not self.province is self.diagram.get_atom(self.x, self.y-1).province: return True
            except AttributeError: return True
        except AssertionError: return True
        return False

    def check_coast(self):
        if self.terrain.con_out<=0.5: return False
        try:
            a = self.diagram.get_atom(self.x+1, self.y)
            if a.terrain.con_out<=0.5: return True
        except AttributeError: pass
        try:
            a = self.diagram.get_atom(self.x-1, self.y)
            if a.terrain.con_out<=0.5: return True
        except AttributeError: pass
        try:
            a = self.diagram.get_atom(self.x, self.y+1)
            if a.terrain.con_out<=0.5: return True
        except AttributeError: pass
        try:
            a = self.diagram.get_atom(self.x, self.y-1)
            if a.terrain.con_out<=0.5: return True
        except AttributeError: pass

    def __repr__(self):
        return "x%d:y%d" % (self.x, self.y)
    

class EmpDiagram:
    def __init__(self, core, width, height):
        self.rgb = [0, 100, 100] * width * height
        self.atoms = [None] * width * height
        self.height = height
        self.width = width
        self.core = core

    def refresh(self):
        for n,a in enumerate(self.atoms):
            if a==None: self.rgb[3*n:3*n+3] = (0, 100, 100)
            else: self.rgb[3*n:3*n+3] = a.terrain.rgb
        
    def get_atom(self, x, y):
        call_error(x<0 or y<0 or x>=self.width or y>=self.height, "out of diagram")
        return self.atoms[x+self.width*y]
    
    def draw_lines(self):
        g = (a for a in self.atoms if a!=None and a.check_coast())        
        for a in g: self.rgb[3*a.n:3*a.n+3] = (0,64,128)
        g = (a for a in self.atoms if a!=None and a.check_border())        
        for a in g: self.rgb[3*a.n:3*a.n+3] = (0,0,0)

                    
    def set_area(self, pixels, p, t):
        for x,y in pixels:
            if x<0 or y<0 or x>=self.width or y>=self.height: return

            i,i3 = x+self.width*y, 3*(x+self.width*y)
            self.atoms[i] = EmpAtom(self, x, y, p, t)
            self.rgb[i3:i3+3] = t.rgb[0:3]
                        
    def dilation(self, pixel, p, t):
        atom = self.get_atom(*pixel)
        if atom == None: return
        if not atom.terrain is t: return
        if not atom.province is p: return
        checked = [False] * self.width * self.height
        to_check,to_change = [pixel],[]
        
        while to_check:
            xy = to_check.pop()
            checked[xy[0] + xy[1]*self.width] = True
            for x,y in [(0,1), (0,-1), (1,0), (-1,0)]:
                nxy = (xy[0]+x,xy[1]+y)
                try:
                    if checked[nxy[0] + nxy[1]*self.width]: continue
                except IndexError: continue
                try: natom = self.get_atom(*nxy)
                except AssertionError: continue
                if natom==None: to_change.append(nxy)
                elif not(atom.province is natom.province): to_change.append(nxy)
                elif not(atom.terrain is natom.terrain): to_change.append(nxy)
                else: to_check.append(nxy)        
        self.set_area(to_change, p, t)

    def set_circle(self, pixel, p, t):
        radius, pixels = 6, []
        for x in range(2*radius+1):
            for y in range(2*radius+1):
                if (x-radius)**2 + (y-radius)**2 > radius**2: continue
                pixels.append((pixel[0]+(x-radius), pixel[1]+(y-radius)))
        self.set_area(pixels, p, t)

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
    def add_terrain(self, name, rgb, con_in, con_out):
        try: nt = EmpTerrain(self, name, rgb, con_in, con_out)
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
    
        
