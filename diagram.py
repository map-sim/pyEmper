#!/usr/bin/python3

from tools import  call_error

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
        if self.terrain.ship<=0.5: return False
        try:
            a = self.diagram.get_atom(self.x+1, self.y)
            if a.terrain.ship<=0.5: return True
        except AttributeError: pass
        try:
            a = self.diagram.get_atom(self.x-1, self.y)
            if a.terrain.ship<=0.5: return True
        except AttributeError: pass
        try:
            a = self.diagram.get_atom(self.x, self.y+1)
            if a.terrain.ship<=0.5: return True
        except AttributeError: pass
        try:
            a = self.diagram.get_atom(self.x, self.y-1)
            if a.terrain.ship<=0.5: return True
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

    def set_atom(self, x, y, atom):
        call_error(x<0 or y<0 or x>=self.width or y>=self.height, "out of diagram")
        self.atoms[x+self.width*y] = None
    
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
                        
    def set_circle(self, pixel, p, t):
        radius, pixels = 6, []
        for x in range(2*radius+1):
            for y in range(2*radius+1):
                if (x-radius)**2 + (y-radius)**2 > radius**2: continue
                pixels.append((pixel[0]+(x-radius), pixel[1]+(y-radius)))
        self.set_area(pixels, p, t)

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
        print("dilatation")

    def filling(self, pixel, p, t):
        if p==None and t==None:
            self.set_atom(*pixel, None)
            
        atom = self.get_atom(*pixel)
        if atom == None: return
        old_p = atom.province
        old_t = atom.terrain

        to_check = [atom]
        checked = []
 
        while to_check:
            a = to_check.pop()
            checked.append(a)
            a.province,a.terrain = p,t

            for x,y in [(0,1), (0,-1), (1,0), (-1,0)]:
                an = self.get_atom(a.x+x,a.y+y)
                if an == None: continue
                elif an in checked: continue
                elif an.province is old_p and an.terrain is old_t:
                    to_check.append(an)
        print("filling")
       
    def smooth_by_province(self):
        for a in self.atoms:
            if a==None:  continue                
            try: provs = [self.get_atom(a.x+1, a.y).province]
            except AttributeError: provs = []
            except AssertionError: provs = []
            try: provs.append(self.get_atom(a.x-1, a.y).province)
            except AttributeError: pass
            except AssertionError: pass
            try: provs.append(self.get_atom(a.x, a.y+1).province)
            except AttributeError: pass
            except AssertionError: pass
            try: provs.append(self.get_atom(a.x, a.y-1).province)
            except AttributeError: pass
            except AssertionError: pass
            
            dp = {}
            for p in provs:
                try: dp[p] += 1
                except KeyError: dp[p] = 1

            for p in dp.keys():
                if dp[p]>2: a.province = p
        print("smooth")
