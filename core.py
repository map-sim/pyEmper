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
        k = self.get_my_id(), self.name, self.con_in, self.con_out, *self.rgb
        return "t%d:%s %g %g (%d,%d,%d)" % k

    def __init__(self, core, name, rgb, con_in, con_out):
        super().__init__(core, name, core.terrains)        
        self.set_parameters(rgb, con_in, con_out)

    def set_parameters(self, rgb, con_in, con_out):
        assert len(rgb) == 3, "3 times char is excpected"
        assert con_in>=0 and con_in<=1, "con_in out of range"
        assert con_out>=0 and con_out<=1, "con_out out of range"
        for c in rgb: assert int(c)>=0 and int(c)<256, "3 chars are excpected"
        self.con_out = float(con_out)
        self.con_in = float(con_in)
        self.rgb = tuple(rgb)
            
class EmpProvince(EmpIder):
    def __repr__(self): return "p%d:%s" % (self.get_my_id(), self.name)
    def __init__(self, core, name):
        super().__init__(core, name, core.provinces)        
            
class EmpNation(EmpIder):
    def __repr__(self): return "n%d:%s" % (self.get_my_id(), self.name)
    def __init__(self, core, name):
        super().__init__(core, name, core.provinces)        

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
        super().__init__(core, name, core.goods)        


class EmpAtom:
    def __init__(self, diagram, x, y, province, terrain):
        self.province = province
        self.terrain = terrain
        self.diagram = diagram
        
        self.n = x + y*self.diagram.width
        self.x,self.y = x,y
        
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

    def __cmp_provinces(self, a1, a2):
        if a1==None and a2==None: return True
        if a1==None or a2==None: return False
        if a1.province is a2.province: return True
        else: return False
    
    def __check_border(self, atom):
        if atom==None: return False
        try:
            if not self.__cmp_provinces(atom, self.get_atom(atom.x+1, atom.y)): return True
            if not self.__cmp_provinces(atom, self.get_atom(atom.x-1, atom.y)): return True
            if not self.__cmp_provinces(atom, self.get_atom(atom.x, atom.y+1)): return True
            if not self.__cmp_provinces(atom, self.get_atom(atom.x, atom.y-1)): return True
        except AssertionError: return True
        return False
        
    def draw_lines(self):
        g1 = (a for a in self.atoms if self.__check_border(a))        
        for a in g1: self.rgb[3*a.n:3*a.n+3] = (0,0,0)
                    
    def set_area(self, pixels, p, t):
        for x,y in pixels:
            if x<0 or y<0 or x>=self.width or y>=self.height: return

            prov = self.core.provinces[p]
            i,i3 = x+self.width*y, 3*(x+self.width*y)
            self.atoms[i] = EmpAtom(self, x, y, prov, self.core.terrains[t])
            self.rgb[i3:i3+3] = self.core.terrains[t].rgb[0:3]
                        
    def set_border(self, pixel, p, t):
        atom = self.get_atom(*pixel)
        if atom == None: return
        if not atom.terrain is self.core.terrains[t]: return
        if not atom.province is self.core.provinces[p]: return
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
        
    def add_terrain(self, name, rgb, con_in, con_out):
        try: nt = EmpTerrain(self, name, rgb, con_in, con_out)
        except AssertionError: return -1

        for t in self.terrains:
            if name==t.name: return -1
        nt.core = self
        self.terrains.append(nt)
        return len(self.terrains)-1 

    def rm_terrain(self, n):
        if n!=len(self.terrains)-1: return 1
        else: del self.terrains[n]
        return 0
    
    def add_province(self, name):
        try: np = EmpProvince(self, name)
        except AssertionError: return -1

        for p in self.provinces:
            if name==p.name: return -1
        np.core = self
        self.provinces.append(np)
        return len(self.provinces)-1 

    def rm_province(self, n):
        if n!=len(self.provinces)-1: return 1
        else: del self.provinces[n]
        return 0
    
    def add_nation(self, name):
        try: nn = EmpNation(self, name)
        except AssertionError: return -1

        for n in self.nations:
            if name==n.name: return -1
        nn.core = self
        self.nations.append(nn)
        return len(self.nations)-1 

    def rm_nation(self, n):
        if n!=len(self.nations)-1: return 1
        else: del self.nations[n]
        return 0
    
    def add_control(self, name):
        try: nc = EmpControl(self, name)
        except AssertionError: return -1

        for c in self.controls:
            if name==c.name: return -1
        nc.core = self
        self.controls.append(nc)
        return len(self.controls)-1 

    def rm_control(self, n):
        if n!=len(self.controls)-1: return 1
        else: del self.controls[n]
        return 0
    
    def add_good(self, name):
        try: ng = EmpGood(self, name)
        except AssertionError: return -1

        for g in self.goods:
            if name==g.name: return -1
        ng.core = self
        self.goods.append(ng)
        return len(self.goods)-1 

    def rm_good(self, n):
        if n!=len(self.goods)-1: return 1
        else: del self.goods[n]
        return 0
    
    def add_process(self, name):
        try: np = EmpProcess(self, name)
        except AssertionError: return -1

        for p in self.processes:
            if name==p.name: return -1
        np.core = self
        self.processes.append(np)
        return len(self.processes)-1
    
    def rm_process(self, n):
        if n!=len(self.processes)-1: return 1
        else: del self.processes[n]
        return 0
