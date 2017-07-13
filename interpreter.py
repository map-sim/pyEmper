#!/usr/bin/python3

import re
import sys
from save import EmpSave

import gi
from gi.repository import Gdk

class EmpInterpreter:

    def __init__(self, editor):
        self.editor = editor
        self.inbuf = []


    def put(self, c):
        if c==65293:
            print()
            if self.inbuf: self.exe()
            self.inbuf = []
        else:            
            if re.match("[a-zA-Z0-9.* +-_?]", str(chr(c))):
                print(chr(c), end="")
                sys.stdout.flush()
                self.inbuf.append(chr(c))
        
    def exe(self):
        line = "".join(c for c in self.inbuf)

        ###########################################################################
        orders = []

        orders.append("p")
        orders.append("t")
        orders.append("n")
        orders.append("c")
        orders.append("g")
        orders.append("s")

        orders.append("p[*]")
        orders.append("t[*]")
        orders.append("n[*]")
        orders.append("c[*]")
        orders.append("g[*]")
        orders.append("s[*]")

        orders.append("p[0-9]+")
        orders.append("t[0-9]+")
        orders.append("n[0-9]+")
        orders.append("c[0-9]+")
        orders.append("g[0-9]+")
        orders.append("s[0-9]+")

        orders.append("p[+]\s*[a-zA-Z_]+")
        orders.append("t[+]\s*[a-zA-Z_]+")
        orders.append("n[+]\s*[a-zA-Z_]+")
        orders.append("c[+]\s*[a-zA-Z_]+")
        orders.append("g[+]\s*[a-zA-Z_]+")
        orders.append("s[+]\s*[a-zA-Z_]+")

        orders.append("p-\s*[a-zA-Z_]+")
        orders.append("t-\s*[a-zA-Z_]+")
        orders.append("n-\s*[a-zA-Z_]+")
        orders.append("c-\s*[a-zA-Z_]+")
        orders.append("g-\s*[a-zA-Z_]+")
        orders.append("s-\s*[a-zA-Z_]+")

        orders.append("p[.]\s*name\s+[a-zA-Z_]+")
        orders.append("t[.]\s*name\s+[a-zA-Z_]+")
        orders.append("n[.]\s*name\s+[a-zA-Z_]+")
        orders.append("c[.]\s*name\s+[a-zA-Z_]+")
        orders.append("g[.]\s*name\s+[a-zA-Z_]+")
        orders.append("s[.]\s*name\s+[a-zA-Z_]+")

        orders.append("t[.]\s*rgb")
        orders.append("t[.]\s*con\s*[0-9]+[.]?[0-9]?")
        orders.append("t[.]\s*ship\s*[0-9]+[.]?[0-9]?")
        orders.append("t\s*swap\s*[0-9]+")

        orders.extend(["[?]", "p[?]", "t[?]"])
        orders.extend(["d", "d[0-5]", "p\s*aa"])
        orders.extend(["r", "rl", "rr"])
        orders.extend(["rgb", "xy"])

        orders.append("save [a-zA-Z0-9_-]+")
        orders.extend(["info", "help"])

        ###########################################################################
        # print obj
        
        if re.match("\Ap\Z", line): print(self.editor.objects["p"])
        elif re.match("\At\Z", line): print(self.editor.objects["t"])
        elif re.match("\An\Z", line): print(self.editor.objects["n"])
        elif re.match("\Ac\Z", line): print(self.editor.objects["c"])
        elif re.match("\Ag\Z", line): print(self.editor.objects["g"])
        elif re.match("\As\Z", line): print(self.editor.objects["s"])

        ###########################################################################
        # print all objs

        elif re.match("\Ap[*]\Z", line):
            for p in self.editor.core.provinces: print(p)
            print("=", len(self.editor.core.provinces), "provinces")
        elif re.match("\At[*]\Z", line):
            for t in self.editor.core.terrains: print(t)
            print("=", len(self.editor.core.terrains), "terrains")
        elif re.match("\An[*]\Z", line):
            for n in self.editor.core.nations: print(n)
            print("=", len(self.editor.core.nations), "nations")
        elif re.match("\Ac[*]\Z", line):
            for c in self.editor.core.controls: print(c)
            print("=", len(self.editor.core.controls), "controls")
        elif re.match("\Ag[*]\Z", line):
            for g in self.editor.core.goods: print(g)
            print("=", len(self.editor.core.goods), "goods")
        elif re.match("\As[*]\Z", line):
            for s in self.editor.core.processes: print(s)
            print("=", len(self.editor.core.processes), "processes")

        ###########################################################################
        # set obj
        
        elif re.match("\Ap[0-9]+\Z", line):
            p_id = int(re.findall("[0-9]+", line)[0])
            self.editor.set_object("p", p_id)
            print(self.editor.objects["p"])
        elif re.match("\At[0-9]+\Z", line):
            t_id = int(re.findall("[0-9]+", line)[0])
            self.editor.set_object("t", t_id)
            print(self.editor.objects["t"])
        elif re.match("\An[0-9]+\Z", line):
            n_id = int(re.findall("[0-9]+", line)[0])
            self.editor.set_object("n", n_id)
            print(self.editor.objects["n"])
        elif re.match("\Ac[0-9]+\Z", line):
            c_id = int(re.findall("[0-9]+", line)[0])
            self.editor.set_object("c", c_id)
            print(self.editor.objects["c"])
        elif re.match("\Ag[0-9]+\Z", line):
            g_id = int(re.findall("[0-9]+", line)[0])
            self.editor.set_object("g", g_id)
            print(self.editor.objects["g"])
        elif re.match("\As[0-9]+\Z", line):
            s_id = int(re.findall("[0-9]+", line)[0])
            self.editor.set_object("s", s_id)
            print(self.editor.objects["s"])

        ###########################################################################
        # add

        elif re.match("\Ap[+]\s*[a-zA-Z_]+\Z", line):
            name = re.findall("[a-zA-Z_]+", line)[1]
            print(self.editor.core.add_province(name))
            
        elif re.match("\At[+]\s*[a-zA-Z_]+\Z", line):
            name = re.findall("[a-zA-Z_]+", line)[1]
            rgb = self.editor.rainbow.get_rgb_color(*self.editor.last_click)
            print(self.editor.core.add_terrain(name, rgb, 0.0, 0.0))

        elif re.match("\An[+]\s*[a-zA-Z_]+\Z", line):
            name = re.findall("[a-zA-Z_]+", line)[1]
            print(self.editor.core.add_nation(name))

        elif re.match("\Ac[+]\s*[a-zA-Z_]+\Z", line):
            name = re.findall("[a-zA-Z_]+", line)[1]
            print(self.editor.core.add_control(name))

        elif re.match("\Ag[+]\s*[a-zA-Z_]+\Z", line):
            name = re.findall("[a-zA-Z_]+", line)[1]
            print(self.editor.core.add_good(name))

        elif re.match("\As[+]\s*[a-zA-Z_]*\Z", line):
            name = re.findall("[a-zA-Z_]+", line)[1]
            print(self.editor.core.add_process(name))

        ###########################################################################
        # sub
        
        elif re.match("\Ap-\s*[a-zA-Z_]+\Z", line):
            p_name = str(re.findall("[a-zA-Z_]+", line)[1])
            if self.editor.objects["p"] and self.editor.objects["p"].name == p_name:
                self.editor.core.rm_province(self.editor.objects["p"].get_my_id())
                self.editor.set_object("p", 0)
                print("rm:", p_name)
            else: print("refuse rm")

        elif re.match("\At-\s*[a-zA-Z_]+\Z", line):
            t_name = str(re.findall("[a-zA-Z_]+", line)[1])
            if self.editor.objects["t"] and self.editor.objects["t"].name == t_name:
                self.editor.core.rm_terrain(self.editor.objects["t"].get_my_id())
                self.editor.set_object("t", 0)
                print("rm:", t_name)
            else: print("refuse rm")

        elif re.match("\An-\s*[a-zA-Z_]+\Z", line):
            n_name = str(re.findall("[a-zA-Z_]+", line)[1])
            if self.editor.objects["n"] and self.editor.objects["n"].name == n_name:
                self.editor.core.rm_nation(self.editor.objects["n"].get_my_id())
                self.editor.set_object("n", 0)
                print("rm:", n_name)
            else: print("refuse rm")

        elif re.match("\Ac-\s*[a-zA-Z_]+\Z", line):
            c_name = str(re.findall("[a-zA-Z_]+", line)[1])
            if self.editor.objects["c"] and self.editor.objects["c"].name == c_name:
                self.editor.core.rm_control(self.editor.objects["c"].get_my_id())
                self.editor.set_object("c", 0)
                print("rm:", c_name)
            else: print("refuse rm")

        elif re.match("\Ag-\s*[a-zA-Z_]+\Z", line):
            g_name = int(re.findall("[a-zA-Z_]+", line)[1])
            if self.editor.objects["g"] and self.editor.objects["g"].name == g_name:
                self.editor.core.rm_good(self.editor.objects["g"].get_my_id())
                self.editor.set_object("g", 0)
                print("rm:", g_name)
            else: print("refuse rm")

        elif re.match("\As-\s*[a-zA-Z_]+\Z", line):
            s_name = str(re.findall("[a-zA-Z_]+", line)[1])
            if self.editor.objects["s"] and self.editor.objects["s"].name == s_name:
                self.editor.core.rm_process(self.editor.objects["s"].get_my_id())
                self.editor.set_object("s", 0)
                print("rm:", s_name)
            else: print("refuse rm")
                        
        ###########################################################################
        # mod (name)
        
        elif re.match("\Ap[.]\s*name\s+[a-zA-Z_]+\Z", line):
            if self.editor.objects["p"]:
                name = re.findall("[a-zA-Z_]+", line)[2]
                self.editor.objects["p"].name = name
                print("mod:", self.editor.objects["p"])
            else: print("not mod")

        elif re.match("\At[.]\s*name\s+[a-zA-Z_]+\Z", line):
            if self.editor.objects["t"]:
                name = re.findall("[a-zA-Z_]+", line)[2]
                self.editor.objects["t"].name = name
                print("mod:", self.editor.objects["t"])
            else: print("not mod")

        elif re.match("\An[.]\s*name\s+[a-zA-Z_]+\Z", line):
            if self.editor.objects["n"]:
                name = re.findall("[a-zA-Z_]+", line)[2]
                self.editor.objects["n"].name = name
                print("mod:", self.editor.objects["n"])
            else: print("not mod")

        elif re.match("\Ac[.]\s*name\s+[a-zA-Z_]+\Z", line):
            if self.editor.objects["c"]:
                name = re.findall("[a-zA-Z_]+", line)[2]
                self.editor.objects["c"].name = name
                print("mod:", self.editor.objects["c"])
            else: print("not mod")

        elif re.match("\Ag[.]\s*name\s+[a-zA-Z_]+\Z", line):
            if self.editor.objects["g"]:
                name = re.findall("[a-zA-Z_]+", line)[2]
                self.editor.objects["g"].name = name
                print("mod:", self.editor.objects["g"])
            else: print("not mod")

        elif re.match("\As[.]\s*name\s+[a-zA-Z_]+\Z", line):
            if self.editor.objects["s"]:
                name = re.findall("[a-zA-Z_]+", line)[2]
                self.editor.objects["s"].name = name
                print("mod:", self.editor.objects["s"])
            else: print("not mod")

        ###########################################################################
        # mod

        elif re.match("\At[.]\s*rgb\Z", line):
            if self.editor.objects["t"]:
                rgb = self.editor.rainbow.get_rgb_color(*self.editor.last_click)
                self.editor.objects["t"].set_rgb(rgb)
                print("mod:", self.editor.objects["t"])
            else: print("not set")
                
        elif re.match("\At[.]con\s*[0-9]+[.]?[0-9]?\Z", line):
            if self.editor.objects["t"]:
                con = re.findall("[0-9]+[.]?[0-9]?", line)[0]
                self.editor.objects["t"].set_con(float(con))
                print("mod:", self.editor.objects["t"])
            else: print("not set")

        elif re.match("\At[.]ship\s*[0-9]+[.]?[0-9]?\Z", line):
            if self.editor.objects["t"]:
                ship = re.findall("[0-9]+[.]?[0-9]?", line)[0]
                self.editor.objects["t"].set_ship(float(ship))
                print("mod:", self.editor.objects["t"])
            else: print("not set")
                
        elif re.match("\At\s*swap\s*[0-9]+\Z", line):
            if self.editor.objects["t"]:                
                n1 = int(re.findall("[0-9]+", line)[0])
                n2 = self.editor.objects["t"].get_my_id()
                try: 
                    self.editor.core.swap_terrains(n1, n2)
                    print("swap")
                except IndexError: print("not swap")
            else: print("not swap")
            
        ###########################################################################
        # get

        elif re.match("\A[?]\Z", line):
            atom = self.editor.core.diagram.get_atom(*self.editor.last_click)
            if atom==None: print("not get")
            else:
                self.editor.set_object("p", atom.province.get_my_id())
                self.editor.set_object("t", atom.terrain.get_my_id())
                print("got")

        elif re.match("\Ap[?]\Z", line):
            atom = self.editor.core.diagram.get_atom(*self.editor.last_click)
            if atom==None: print("not get")
            else:
                self.editor.set_object("p", atom.province.get_my_id())
                if atom==None: print("get")
                
        elif re.match("\At[?]\Z", line):
            atom = self.editor.core.diagram.get_atom(*self.editor.last_click)
            if atom==None: print("not get")
            else:
                self.editor.set_object("t", atom.terrain.get_my_id())
                if atom==None: print("get")

        ###########################################################################
        # pen

        elif re.match("\Ad[0-5]\Z", line):
            n = int(re.findall("[0-5]", line)[0])
            self.editor.objects["d"]=n
            label = self.editor.pens[self.editor.objects["d"]]
            self.editor.labels["d"].set_text("d:"+label)
            print("pen:", label)

            if n==5: cursor = Gdk.Cursor(Gdk.CursorType.BOX_SPIRAL)
            elif n in [1,2,3]: cursor = Gdk.Cursor(Gdk.CursorType.CROSS)
            elif n==4: cursor = Gdk.Cursor(Gdk.CursorType.TARGET)
            else: cursor = Gdk.Cursor(Gdk.CursorType.DOT)
            gdk_window = self.editor.get_root_window()
            gdk_window.set_cursor(cursor)

        elif re.match("\Ad\Z", line):
            self.editor.objects["d"]=0
            label = self.editor.pens[self.editor.objects["d"]]
            self.editor.labels["d"].set_text("d:"+label)
            print("pen:", label)

            cursor = Gdk.Cursor(Gdk.CursorType.DOT)
            gdk_window = self.editor.get_root_window()
            gdk_window.set_cursor(cursor)
        
        elif re.match("\Ap\s*aa\Z", line):           
            self.editor.core.diagram.smooth_by_province()
            print("aa")
            
        ###########################################################################
        # screen

        elif re.match("\Ar\Z", line):
            self.editor.diagram_rgb = self.editor.core.diagram.rgb
            self.editor.core.diagram.refresh()
            self.editor.refresh()

        elif re.match("\Arr\Z", line):
            self.editor.diagram_rgb = self.editor.rainbow.rgb
            self.editor.refresh()

        elif re.match("\Arl\Z", line):
            self.editor.diagram_rgb = self.editor.core.diagram.rgb
            self.editor.core.diagram.refresh()
            self.editor.core.diagram.draw_lines()        
            self.editor.refresh()

        ###########################################################################
        # settings

        elif re.match("\Argb\Z", line):
            r,g,b = self.editor.rainbow.get_rgb_color(*self.editor.last_click)
            print("rgb:", r, g, b)

        elif re.match("\Axy\Z", line):           
            print("xy:", *self.editor.last_click)

        ###########################################################################
        # other

        elif re.match("\Asave [a-zA-Z0-9_-]+\Z", line):           
            name = re.findall("[a-zA-Z0-9_-]+", line)[1]
            s = EmpSave(self.editor.core, name+".db")
            s.expotr_to_html()

        elif re.match("\Ainfo\Z", line):           
            print("Author: Krzysztof Czarnecki, Gdansk, Poland")
            print("Email: czarnecki.krzysiek@gmail.com")
            print("If you like my work, please send me an email.")

        elif re.match("\Ahelp\Z", line):           
            for o in orders: print(o)

        else: print("command not matched:", line)
