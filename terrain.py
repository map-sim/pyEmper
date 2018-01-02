#! /usr/bin/python3

import os


def EmpTerrainGen(fname):
    if not os.path.exists(fname):
        raise ValueError("file %s not exists" % fname)
    if fname[-4:] != ".txt" and  fname[-4:] != ".TXT":
        raise ValueError("file %s not looks as TXT" % fname)

    tmp_rgb = set()
    tmp_name = set()
    with open(fname) as fd:
        while True:
            try:
                line = fd.readline()
                if "#" in line:
                    continue
                name, con, rgb = line.split(";")
                con, wet = con.split()
                rgb = rgb.split()
                rgb = tuple([int(c, 16) for c in rgb])
            except ValueError:
                raise StopIteration
                
            if name in tmp_name:
                raise GeneratorExit("name %s in terrains is doubled" % name)
            tmp_name.add(name)
                    
            if rgb in tmp_rgb:
                raise GeneratorExit("rgb %s in terrains is doubled" % str(rgb))
            tmp_rgb.add(rgb)
                
            yield EmpTerrain(name, con, wet, rgb)

            
class EmpTerrains(set):
    def __init__(self, fname):
        gen = EmpTerrainGen(fname)
        set.__init__(self, gen)

        self.proxy = {}
        for t in self:
            self.proxy[t.name] = t
        
    def get_by_name(self, name):
        return self.proxy[name]
        
    def save(self, fname):
        with open(fname, "w") as fd:
            for t in self:
                fd.write(str(t))
                fd.write("\n")
        

class EmpTerrain:
    def __init__(self, name, con, wet, rgb):
        self.name = str(name)

        if float(con)<0 or float(con)>1:
            raise ValueError("con has wrong value")
        self.con = float(con)
        
        if float(wet)<0 or float(wet)>1:
            raise ValueError("wet has wrong value")
        self.wet = float(wet)
        
        if not isinstance(rgb, (tuple, list)):
            raise TypeError("no rgb collection")
        self.rgb = rgb

    def __sub__(self, rgb):
        if isinstance(rgb, (EmpTerrain, )):
            rgb = rgb.rgb
        if not isinstance(rgb, (tuple, list)):
            raise TypeError("no rgb collection")

        out = 0
        for i, j in zip(self.rgb, rgb):
            out += abs(i - j)
        return out

    def __str__(self):
        out = self.name + "; "
        out += "%g %g; " % (self.con, self.wet)
        out += "%s %s %s" % tuple([hex(c) for c in self.rgb])
        return out

    

