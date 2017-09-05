#!/usr/bin/python3

from tools import  call_error
import random

class EmpAtom:
    def __repr__(self): return "x%d:y%d" % (self.x, self.y)
    def __init__(self, diagram, x, y, province, terrain):
        self.province = province
        self.terrain = terrain
        self.diagram = diagram
        self.set_xy(x,y)

    def set_xy(self, x, y):
        self.n = x + y*self.diagram.width
        self.x,self.y = x,y

    def get_xy(self):
        return (self.x, self.y)

    def check_border(self):        
        for x,y in [(0,1), (0,-1), (1,0), (-1,0)]:
            try:
                if not self.province is self.diagram.get_atom(self.x+x, self.y+y).province:
                    return True
            except AttributeError: return True     
            except AssertionError: pass

    def check_coast(self):
        if self.terrain.ship<=0.5: return False
        for x,y in [(0,1), (0,-1), (1,0), (-1,0)]:

            try:
                a = self.diagram.get_atom(self.x+x, self.y+y)
                if a.terrain.ship<=0.5: return True
            except AttributeError: return True
            except AssertionError: pass

    
class EmpDiagram:
    def __init__(self, core, width, height):
        self.rgb = [0, 100, 100] * width * height
        self.atoms = [None] * width * height
        self.height = height
        self.width = width
        self.core = core

    def get_xy(self, n):
        x = int(n % self.width)
        y = int(n / self.width)
        return x,y
        
    def move_roller(self, delta):
        moved_atoms = [None] * self.width * self.height
        g = (a for a in self.atoms if a!=None)        
        for a in g:
            nx = (a.x+delta) % self.width
            a.set_xy(nx, a.y)
            n = a.x+self.width*a.y
            moved_atoms[n] = a
        self.atoms = moved_atoms
        self.refresh()
        


    def refresh(self):
        for n,a in enumerate(self.atoms):
            if a==None: self.rgb[3*n:3*n+3] = (0, 100, 100)
            else: self.rgb[3*n:3*n+3] = a.terrain.rgb
        
    def get_atom(self, x, y):
        call_error(x<0 or y<0 or x>=self.width or y>=self.height, "out of diagram")
        return self.atoms[x+self.width*y]

    def draw_lines(self, rgb):
        g = (a for a in self.atoms if a!=None and a.check_coast())        
        for a in g: rgb[3*a.n:3*a.n+3] = (0,64,128)
        g = (a for a in self.atoms if a!=None and a.check_border())        
        for a in g: rgb[3*a.n:3*a.n+3] = (0,0,0)

    def draw_population(self, nation):
        rgb = [255, 255, 255] * self.width * self.height
        max_pop = 0
        for p in self.core.provinces:
            if p.population[nation]>max_pop:
                max_pop = p.population[nation]
        if max_pop==0: return rgb
        
        g = (a for a in self.atoms if a!=None)        
        for a in g:
            if a.terrain.ship>0.5: rgb[3*a.n:3*a.n+3] = (0,255,255)
            else:
                f = a.province.population[nation]/max_pop
                if f==0:
                    r,g,b = 0,200,200
                elif f<0.66:
                    r = 255
                    g = 255-int(255*1.5*f)
                    b = 255-int(255*1.5*f)
                else:
                    r = 255-int(255*2*(f-0.66))
                    b = 0
                    g = 0
                rgb[3*a.n:3*a.n+3] = (r,g,b)

        return rgb
            
    def set_area(self, pixels, p, t):
        for x,y in pixels:
            if x<0 or y<0 or x>=self.width or y>=self.height:
                continue

            i,i3 = x+self.width*y, 3*(x+self.width*y)
            if p==None or t==None:
                self.atoms[i] = None
                self.rgb[i3:i3+3] = (0, 100, 100)
            else:
                self.atoms[i] = EmpAtom(self, x, y, p, t)
                self.rgb[i3:i3+3] = t.rgb[0:3]
                        
    def set_circle(self, pixel, p, t, r=6):
        pixels = []
        for x in range(2*r+1):
            for y in range(2*r+1):
                if (x-r)**2 + (y-r)**2 > r**2: continue
                pixels.append((pixel[0]+(x-r), pixel[1]+(y-r)))
        self.set_area(pixels, p, t)
        
    def set_blur(self, pixel, p, t):
        for n in range(5):
            x = random.randint(-9,9) +pixel[0]
            y = random.randint(-9,9) +pixel[1]
            self.set_circle((x,y), p, t, 6)

            for n in range(4):
                xx = random.randint(-5,5) +x
                yy = random.randint(-5,5) +y
                self.set_circle((xx,yy), p, t, 3)


    def get_area(self, pixel):
        atom = self.get_atom(*pixel)
        if atom == None:
            print("None cannot be got")
            return []

        checked = []
        to_check = [atom]
        found = [atom.get_xy()]
        
        while to_check:
            a = to_check.pop()
            checked.append(a)
            for x,y in [(0,1), (0,-1), (1,0), (-1,0)]:
                try:
                    an = self.get_atom(a.x+x,a.y+y)
                    if an in checked: continue
                    elif an.province is atom.province and an.terrain is atom.terrain:
                        to_check.append(an)
                        found.append(an.get_xy())
                except AttributeError: continue
                except AssertionError: continue
        return found 

    def smooth_by_province(self):
        for a in self.atoms:
            if a==None:  continue
            provs = []
            for x,y in [(0,1), (0,-1), (1,0), (-1,0)]:
                try: provs.append(self.get_atom(a.x+x, a.y+y).province)
                except AttributeError: continue
                except AssertionError: continue
            
            dp = {}
            for p in provs:
                try: dp[p] += 1
                except KeyError: dp[p] = 1

            for p in dp.keys():
                if dp[p]>2: a.province = p
        print("smooth")

    def smooth_none_poits(self):
        for n,a in enumerate(self.atoms):
            if a!=None:  continue
            bx,by = self.get_xy(n)
            provs = []
            terrs = []
            nexts = 0
            for x,y in [(0,1), (0,-1), (1,0), (-1,0)]:
                try: 
                    provs.append(self.get_atom(bx+x, by+y).province)
                    terrs.append(self.get_atom(bx+x, by+y).terrain)
                    nexts += 1
                except AttributeError: continue
                except AssertionError: continue
            if nexts<3: continue

            dp = {}
            for p in provs:
                try: dp[p] += 1
                except KeyError: dp[p] = 1
            dt = {}
            for t in terrs:
                try: dt[t] += 1
                except KeyError: dt[t] = 1
                
            for p in dp.keys(): 
                if dp[p]>2: prov = p
            for t in dt.keys(): 
                if dt[t]>2: terr = t
            self.set_area([(bx, by)], p, t)
