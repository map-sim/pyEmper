#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import ToolBox
import math

class VectorDiagram(dict):

    def __init__(self, drows, prows, trows):
        dict.__init__(self)
        self.config = {
            prow["name"]: prow["value"]
            for prow in prows
        }

        self.nodes = {}
        for drow in drows:
            col = drow["color"]
            node = drow["node"]
            dx = drow["dx"]
            dy = drow["dy"]
            xykey = drow["x"], drow["y"]
            self[xykey] = col, node, (dx, dy)
            try: self.nodes[node].append(xykey)
            except KeyError: self.nodes[node] = [xykey]
    
        self.terrbox = {
            trow["color"]: (trow["drag"], trow["charge"], trow["aperture"])
            for trow in trows
        }

    def next_atom_generator(self, x, y):
        for dx, dy in ToolBox.unit_generator():
            ny = y + dy
            if ny < 0 or ny >= self.config["map_height"]:
                continue
            nx = (x + dx) % self.config["map_width"]
            yield nx, ny

    def get_next_nodes_as_set(self, node):
        xyset = self.get_node_coordinates_as_set(node, True)
        nodeset = set()
        for xy in xyset:
            n = self.get_node(*xy)
            nodeset.add(n)
        nodeset.remove(node)
        return nodeset

    def get_node_coordinates_as_set(self, node, border=False):
        xyset = set()
        if border:
            for xy, val in self.items():
                if val[1] != node: continue
                xyset |= set(self.next_atom_generator(*xy))
                xyset.add(xy)            
            return xyset
        for xy, val in self.items():
            if val[1] == node: xyset.add(xy)                
        return xyset

    __node_center_cache = {}
    def get_node_center(self, node):
        try: return self.__node_center_cache[node]
        except KeyError: pass

        xyset = self.get_node_coordinates_as_set(node)
        xo, yo = 0, 0
        for x, y in xyset:
            xo, yo = xo+x, yo+y
        self.__node_center_cache[node] = xo/len(xyset), yo/len(xyset)
        return self.__node_center_cache[node]

    def calc_node_distance2(self, n1, n2):
        if n1 == n2: return 0.0
        x1, y1 = self.get_node_center(n1)
        x2, y2 = self.get_node_center(n2)
        return (x1 - x2) ** 2 + (y1 -y2) ** 2
        
    def get_node_border_coordinates_as_set(self, start, stop):
        stopset = self.get_node_coordinates_as_set(stop, True)
        startset = self.get_node_coordinates_as_set(start)
        border = stopset & startset
        return border 
        
    def check_border(self, x, y):
        width = self.config["map_width"]
        borderset = set()

        def fake(self, borderset, x, y, x2, y2, C, c):
            try:
                if self[x, y][1] != self[x2, y2][1]:
                    borderset.add(C)
                if self.check_buildable(x, y) != self.check_buildable(x2, y2):
                    borderset.add(c)
            except KeyError: pass
        fake(self, borderset, x, y, x, y+1, "S", "s")
        fake(self, borderset, x, y, x, y-1, "N", "n")
        fake(self, borderset, x, y, (x+1) % width, y, "W", "w")
        fake(self, borderset, x, y, (x-1) % width, y, "E", "e")
        return borderset

    def get_node(self, x, y): return self[x, y][1]
    def get_color(self, x, y): return self[x, y][0]
    def get_current(self, x, y): return self[x, y][2]
        
    def check_coast(self, x, y):
        fc = lambda x, y, a, b: self.check_buildable(x, y) != self.check_buildable(a, b)
        for nx, ny in self.next_atom_generator(x, y):
            if fc(x, y, nx, ny): return True
        return False

    def check_land(self, node):
        try:
            xy = self.nodes[node][0]
            return self.check_buildable(*xy)
        except KeyError: raise ValueError("(e) no node")

    def check_navigable(self, x, y):
        color = self.get_color(x, y)
        drag = self.terrbox[color][0]
        return drag < 0
        
    def check_buildable(self, x, y):
        color = self.get_color(x, y)
        aperture = self.terrbox[color][2]
        return aperture > 0
    
    def calc_color(self, x, y, current):
        if current:
            return self.calc_current_color(x, y)
        rgb = self[x, y][0]                
        rgbt = [
            int(rgb[2*n:2*n+2], 16)
            for n in range(3)]
        return rgbt

    def calc_current_color(self, x, y):
        dx, dy = self[x,y][2]
        cx, cy = 127 * dx, 127 * dy
        r, g, b = 127 + cx, 127 + cy, 127
        return (r, g, b)

    def __calc_unit_resistance(self, xo, yo, xe, ye):
        co, no, do = self[xo, yo]           
        ce, ne, de = self[xe, ye]

        ro, re = self.terrbox[co][0], self.terrbox[ce][0]
        rOUT = abs(re) * self.config["toll_transport"]

        if xo - xe > 1: xo, xe = 1, 0
        elif xo - xe < -1: xo, xe = 0, 1
        sx = math.copysign(de[0] * (xe - xo), (xo - xe) * de[0])
        rOUT *= self.config["toll_current"] ** sx
        
        sy = math.copysign(de[1] * (ye - yo), (yo - ye) * de[1])
        rOUT *= self.config["toll_current"] ** sy

        if ro * re < 0:
            rOUT += abs(re - ro) * self.config["toll_transship"]            
        return rOUT

    def __plazming(self, startPoints, nodePoints):        
        active = set()
        plazma = dict()        
        for x, y in startPoints:            
            c, n, d = self[x, y]           
            r = self.terrbox[c][0]
            plazma[x, y] = abs(r)
            active.add((x, y))
        width = self.config["map_width"]
        height = self.config["map_height"]

        while active:
            try: x, y = active.pop()
            except KeyError: break

            for nx, ny in self.next_atom_generator(x, y):
                if (nx, ny) not in nodePoints: continue 
                
                uR = self.__calc_unit_resistance(x, y, nx, ny)
                nR = plazma[x, y] + uR
                if not (nx, ny) in plazma.keys():
                    plazma[nx, ny] = nR
                    active.add((nx, ny))     
                elif nR < plazma[nx, ny]:
                    plazma[nx, ny] = nR
                    active.add((nx, ny))
        return plazma

    def calc_enter_resistance(self, start, stop):
        border = self.get_node_border_coordinates_as_set(start, stop)
        if len(border) == 0: return 0.0

        stopatoms = self.get_node_coordinates_as_set(stop, True)
        nodeatoms = self.get_node_coordinates_as_set(stop, False)
        plazma = self.__plazming(border, stopatoms)        
        assert len(stopatoms) == len(plazma), "(e) node discontinuity!"

        # maxp = math.log10(max(plazma.values()))
        # minp = math.log10(min(plazma.values()))
        # for p, v in plazma.items():
        #     c, n, d = self[p]
        #     s = hex(int(255 * (math.log10(v) - minp) / (maxp - minp)))[2:]
        #     if len(s) == 1: s = f"0{s}"
        #     self[p] = "00"+2*s , n, d
        
        rezistance = 0.0
        for xy, rez in plazma.items():
            if xy in nodeatoms:
                rezistance += rez
        lrez = rezistance ** self.config["toll_reductor"]
        drez = lrez ** self.config["toll_distribution"]
        return drez * self.config["map_scale"]
    
    def calc_transit_resistance(self, start, tranz, stop):
        iborder = self.get_node_border_coordinates_as_set(start, tranz)
        oborder = self.get_node_border_coordinates_as_set(stop, tranz)
        if len(iborder) == 0 or len(oborder) == 0: return 0.0

        tranzatoms = self.get_node_coordinates_as_set(tranz, True)
        plazma = self.__plazming(iborder, tranzatoms)
        assert len(tranzatoms) == len(plazma), "(e) node discontinuity!"

        # maxp = math.log10(max(plazma.values()))
        # minp = math.log10(min(plazma.values()))
        # for p, v in plazma.items():
        #     c, n, d = self[p]
        #     s = hex(int(255 * (math.log10(v) - minp) / (maxp - minp)))[2:]
        #     if len(s) == 1: s = f"0{s}"
        #     self[p] = s + "00" + s , n, d

        rezistance = 0.0
        for xy in oborder:
            rezistance += plazma[xy]            
        lrez = (rezistance / len(oborder)) ** self.config["toll_reductor"]
        return lrez * self.config["map_scale"]
