#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import os, sys
import math

import sqlite3
import ToolBox
import VectorDiagram

class BusyBoxSQL:
    __ints = ["map_width", "map_height", "map_project"]
    
    def __init__(self, fname):
        if not os.path.exists(fname):
            ToolBox.print_error(f"path {fname} not exists!")
            sys.exit(-1)
        self.db_name = fname
            
        def dict_factory(cur, row):
            gen = enumerate(cur.description)
            out = {c[0]: row[i] for i,c in gen}
            return out

        self.conn = sqlite3.connect(fname)
        self.conn.row_factory = dict_factory
        self.cur = self.conn.cursor()

    def __del__(self):
        try:
            self.conn.commit()
            self.conn.close()
        except AttributeError:
            pass
        
    def execute(self, query):        
        self.cur.execute(query)
        return self.cur.fetchall()
    
    ###
    ### config specific
    ###
    
    def get_config_by_name(self, name):
        out = self.execute(f"SELECT value FROM config WHERE name='{name}'")
        assert len(out) == 1, "(e) outlen != 1"
        if name in self.__ints:
            return int(out[0]["value"])
        else: return out[0]["value"]

    def set_config_by_name(self, name, value):
        self.execute(f"UPDATE config SET value={value} WHERE name='{name}'")
        if self.cur.rowcount == 0:
            self.execute(f"INSERT INTO config(name, value) VALUES ('{name}', {value})")
        
    def delete_config_by_name(self, name):
        self.execute(f"DELETE FROM config WHERE name='{name}'")

    def get_config_as_dict(self):
        out = self.execute("SELECT * FROM config")
        assert len(out) > 0, "(e) config length < 1"

        dout = {}
        for drow in out:
            if drow['name'] in self.__ints:                
                dout[drow['name']] = int(drow['value'])
            else: dout[drow['name']] = drow['value']
        return dout

    ###
    ### terrain specific
    ###

    def get_colors_as_list(self):
        out = self.execute(f"SELECT color FROM terrain")
        return [drow["color"] for drow in out]

    def get_terrain_as_dict(self, color):
        out = self.execute(f"SELECT * FROM terrain WHERE color='{color}'")
        assert len(out) == 1, "(e) only 1 terrain is expected"
        return out[0]

    ###
    ### diagram specific
    ###

    def get_node_names_as_set(self):
        out = self.execute("SELECT node FROM diagram")
        assert len(out) > 0, "(e) node number < 1"
        nodeset = set()
        for drow in out:
            nodeset.add(drow["node"])
        return nodeset
        
    def get_vector_diagram(self):
        dout = self.execute("SELECT * FROM diagram")
        assert len(dout) > 0, "(e) diagram length < 1"
        tout = self.execute("SELECT * FROM terrain")
        assert len(tout) > 0, "(e) terrains number < 1"
        cout = self.execute("SELECT * FROM config")
        assert len(cout) > 0, "(e) config length < 1"
        return VectorDiagram.VectorDiagram(dout, cout, tout)

    def get_node_coordinates_as_set(self, node):
        out = self.execute(f"SELECT x, y FROM diagram WHERE node='{node}'")
        assert len(out) > 0, "(e) node atom number < 1"

        xyset = set()
        for drow in out:
            item = drow["x"], drow["y"]
            xyset.add(item)
        return xyset

    def get_node_atoms_as_dict(self, node):
        out = self.execute(f"SELECT * FROM diagram WHERE node='{node}'")
        assert len(out) > 0, "(e) node atom number < 1"
        
        atoms = {}
        for drow in out:
            item = drow["x"], drow["y"]
            atoms[item] = drow["color"], drow["dx"], drow["dy"]
        return atoms

    def set_node_by_coordinates(self, x, y, node):
        self.execute(f"UPDATE diagram SET node='{node}' WHERE x={x} AND y={y}")
        self.conn.commit()

    def set_color_by_coordinates(self, x, y, color):
        self.execute(f"UPDATE diagram SET color='{color}' WHERE x={x} AND y={y}")
        self.conn.commit()

    ###
    ### distribution specific
    ###
    
    def set_distribution_by_node(self, node, column, value):
         self.execute(f"UPDATE distribution SET {column}={value} WHERE node='{node}'")
         assert self.cur.rowcount == 1, "(e) column cannot be set"
     
    def clean_distribution(self, column):
        self.execute(f"UPDATE distribution SET {column}=0")
        assert self.cur.rowcount > 0, "(e) column cannot be set"
     
    def get_distribution_by_node(self, node, column):
        out = self.execute(f"SELECT {column} FROM distribution WHERE node='{node}'")
        assert len(out) == 1 or len(out) == 0, "(e) outlen != 1"
        if len(out) == 1: return out[0][column]
        else: return 0

    def get_max_distribution(self, column):
        out = self.execute(f"SELECT MAX({column}) FROM distribution")
        assert len(out) == 1, "(e) outlen != 1"
        return list(out[0].values())[0]

    def get_distribution_as_dict(self, column):
        out = self.execute(f"SELECT node,{column} FROM distribution")
        assert len(out) > 0, "(e) outlen <= 0"
        return {drow['node']: drow[column] for drow in out}

    def get_distribution_as_list(self, node, *keys):
        columns = f",".join(keys)
        where = f"WHERE node='{node}'"
        rows = self.execute(f"SELECT {columns} FROM distribution {where}")
        assert len(rows) == 1, "(e) outlen != 1"
        return [rows[0][key] for key in keys] 
    
    ###
    ### population specific
    ###

    def get_nation_names_as_set(self):
        out = self.execute("PRAGMA table_info(population)")
        cols = set(col["name"] for col in out if col["name"] != "node")
        return cols
    
    def set_population_by_node(self, node, nation, value):
        self.execute(f"UPDATE population SET {nation}={value} WHERE node='{node}'")
        assert self.cur.rowcount == 1, "(e) population cannot be set"

    def clean_population(self, nation):
        self.execute(f"UPDATE population SET {nation}=0")
        assert self.cur.rowcount > 0, "(e) population cannot be set"

    def get_population_by_node_as_dict(self, node):
        out = self.execute(f"SELECT * FROM population WHERE node='{node}'")
        assert len(out) == 1, "(e) outlen != 1"
        return out[0]
    
    def get_population_by_node(self, node, nation=None):
        if nation:        
            out = self.execute(f"SELECT {nation} FROM population WHERE node='{node}'")
            assert len(out) == 1, "(e) outlen != 1"
            return out[0][nation]

        sumc = "+".join(self.get_nation_names_as_set())
        out = self.execute(f"SELECT {sumc} FROM population WHERE node='{node}'")
        assert len(out) > 0, "(e) outlen <= 0"
        return list(out[0].values())[0]

    def get_max_population(self, nation=None):
        if nation:        
            out = self.execute(f"SELECT MAX({nation}) FROM population")
            assert len(out) == 1, "(e) outlen != 1"
            return list(out[0].values())[0]

        sumc = "+".join(self.get_nation_names_as_set())
        out = self.execute(f"SELECT MAX({sumc}) FROM population")
        assert len(out) == 1, "(e) outlen != 1"
        return list(out[0].values())[0]

    def get_population_as_dict(self, nation=None):
        if nation:        
            out = self.execute(f"SELECT node,{nation} FROM population")
            assert len(out) > 0, "(e) outlen <= 0"
            return {drow['node']: drow[nation] for drow in out}

        sumc = "+".join(self.get_nation_names_as_set())
        out = self.execute(f"SELECT node,{sumc} FROM population")
        assert len(out) > 0, "(e) outlen <= 0"
        return {drow['node']: drow[sumc] for drow in out}

    ###
    ### control specific
    ###

    def set_capital_node(self, control, node):
        self.execute(f"UPDATE control SET capital='{node}' WHERE name='{control}'")
        assert self.cur.rowcount == 1, "(e) capital cannot be set"
    def get_capital_node(self, control):
        rows = self.execute(f"SELECT capital FROM control WHERE name='{control}'")
        assert self.cur.rowcount == 1, "(e) capital cannot be taken"
        return rows[0]["capital"]

    def check_control_capital(self, node):
        rows = self.execute(f"SELECT name, capital FROM control")
        controls = {row["name"] for row in rows if node == row["capital"]}
        return controls
        
    def get_controls_as_dict(self, *keys):
        columns = f",".join(keys)
        rows = self.execute(f"SELECT name,{columns} FROM control")
        output = dict()
        for row in rows:
            output[row["name"]] = [row[key] for key in keys]
        return output

    def get_opinion_as_dict(self, control):
        out = self.execute(f"SELECT * FROM opinion WHERE control='{control}'")
        del out[0]["control"]
        return out[0]
        
    def set_opinion_by_control(self, control, nation, value):
        self.execute(f"UPDATE opinion SET {nation}={value} WHERE control='{control}'")
        if self.cur.rowcount == 0:
            self.execute(f"INSERT INTO opinion (control, '{nation}') VALUES ('{control}', {value})")
        assert self.cur.rowcount == 1, "(e) column cannot be set"
    
    ###
    ### force
    ###
        
    def get_force_by_node_as_dict(self, node):
        rows = self.execute(f"SELECT control, value FROM force WHERE node='{node}'")
        output = {row["control"]: row["value"] for row in rows}
        return output
    
    ###
    ### extra
    ###

    def calc_production(self, node):
        pop = self.get_population_by_node(node)        
        pf = self.get_config_by_name("production_factor")
        try:
            r, f = self.get_distribution_as_list(node, "resourcing", "industry")
            production = pf * math.sqrt(pop) * r * (f + 1.0)
            return production
        except AssertionError:
            return 0.0

    def calc_control(self, node):
        nationset = self.get_nation_names_as_set()
        population = self.get_population_by_node(node)

        natdict = {}
        ntmp = self.get_population_by_node_as_dict(node)
        for n in nationset:
            if ntmp[n] > 0: natdict[n] = ntmp[n] / population

        forcedict = self.get_force_by_node_as_dict(node)
        capitalset = self.check_control_capital(node)
        
        opinion_im = 0.4
        force_im = 0.6

        all_force = 0.0
        controls = set(capitalset)
        for c, f in  forcedict.items():
            controls.add(c)            
            all_force += f

        output = {}
        total_opinion = 0.0
        for c in controls:
            tmp = 0.0
            opinion = self.get_opinion_as_dict(c)
            for n, p in natdict.items():
                val = p * opinion[n]
                total_opinion += val
                tmp +=  val
            output[c] = tmp  

        for c in controls:
            output[c] *= opinion_im
            output[c] /= total_opinion
            if c in forcedict.keys():
                fin = forcedict[c] / all_force
            else: fin = 0.0
            output[c] += force_im * fin 
        return output
