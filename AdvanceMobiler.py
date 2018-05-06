#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


from tools import print_info

class AdvanceMobiler:

    def get_common_points(self, startname, stopname):
        commonpoints = set()
        for x,y in self.nodepoints_generator(stopname):    
            for dx,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                try:
                    if self.is_node(x+dx, y+dy, startname):
                        commonpoints.add((x+dx, y+dy))
                except KeyError: continue
        return commonpoints
    
    def calc_transit(self, startname, proxyname, stopname):
        infra_next_transship = self.select_node(stopname, "infra_transship")[0]
        infra_transport = self.select_node(proxyname, "infra_transport")[0]
        infra_transship = self.select_node(proxyname, "infra_transship")[0]
        world_transport = self.get_parameter("transport")
        world_transship = self.get_parameter("transship")
        world_scale =  self.get_parameter("scale")

        startpoints = self.get_common_points(startname, proxyname)
        stoppoints = self.get_common_points(proxyname, stopname)
        print_info("start points: %d" % len(startpoints))
		
        plazma = {}
        active = set()	
        for xy in startpoints:
            plazma[xy] = 0.0
            active.add(xy)
	
        while active:
            try: xy = active.pop()
            except KeyError: break
	
            for dx,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                x, y = xy[0] + dx, xy[1] + dy
	        
                try:
                    
                    if self.diagram[(x, y)][0] != proxyname and \
                       self.diagram[xy][0] != proxyname:
                        continue

                    else:
                        base1,ship1,build1,cost1 = self.get_terrparams(*xy)
                        base2,ship2,build2,cost2 = self.get_terrparams(x, y)
                        np = plazma[xy] +  base2 * world_transport ** (-build2 * infra_transport)
                        np +=  abs(ship2 - ship1) * world_transship ** (-build2 * infra_transship)
                            
                    if not (x, y) in plazma.keys() or np < plazma[(x, y)]:
                        plazma[(x, y)] = np
                        active.add((x, y))

                except KeyError: continue

        output = 0.0
        for xy in stoppoints:
            output += plazma[xy]
	
        try:
            return world_scale * output / len(stoppoints)
        except ZeroDivisionError:
            return float("inf")

        
    def calc_enter(self, startnames, stopname):
        infra_transport = self.select_node(stopname, "infra_transport")[0]
        infra_transship = self.select_node(stopname, "infra_transship")[0]
        infra_fortress = self.select_node(stopname, "infra_fortress")[0]
        world_transport = self.get_parameter("transport")
        world_transship = self.get_parameter("transship")
        world_scale =  self.get_parameter("scale")

        startpoints = set()
        for nodename in startnames:
            for x,y in self.get_common_points(nodename, stopname):
                startpoints.add((x,y))
        print_info("start points: %d" % len(startpoints))
                
        plazma = {}
        active = set()	
        for xy in startpoints:
            plazma[xy] = 0.0
            active.add(xy)
	
        while active:
            try: xy = active.pop()
            except KeyError: break
	
            for dx,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                x, y = xy[0] + dx, xy[1] + dy
	        
                try:
                    
                    if self.diagram[(x, y)][0] != stopname and \
                       self.diagram[xy][0] != stopname:
                        continue

                    else:
                        base1,ship1,build1,cost1 = self.get_terrparams(*xy)
                        base2,ship2,build2,cost2 = self.get_terrparams(x, y)
                        np = plazma[xy] +  base2 * world_transport ** (-build2 * infra_transport)
                        np +=  abs(ship2 - ship1) * world_transship ** (-build2 * infra_transship)
                            
                    if not (x, y) in plazma.keys() or np < plazma[(x, y)]:
                        plazma[(x, y)] = np
                        active.add((x, y))

                except KeyError: continue
                
        output = 0.0
        for xy in plazma.keys():
            if self.diagram[xy][0] == stopname:
                output += plazma[xy]

        return world_scale * output * (1.0 + infra_fortress)
