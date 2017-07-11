#!/usr/bin/python3

import re
from save import EmpSave

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
            if re.match("[a-zA-Z0-9.* _+-]", str(chr(c))):
                self.inbuf.append(chr(c))
        
    def exe(self):
        line = "".join(c for c in self.inbuf)
        
        ###########################################################################
        # set obj
        
        if re.match("\Ap[0-9]+\Z", line):
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
        # print obj
        
        elif re.match("\Ap\Z", line): print(self.editor.objects["p"])
        elif re.match("\At\Z", line): print(self.editor.objects["t"])
        elif re.match("\An\Z", line): print(self.editor.objects["n"])
        elif re.match("\Ac\Z", line): print(self.editor.objects["c"])
        elif re.match("\Ag\Z", line): print(self.editor.objects["g"])
        elif re.match("\As\Z", line): print(self.editor.objects["s"])

        ###########################################################################
        # add

        elif re.match("\Ap[+]\s*[a-zA-Z]+[ ]*[a-zA-Z]*\Z", line):
            name = re.findall("[a-zA-Z ]+", line)[1]
            print(self.editor.core.add_province(name))
            
        elif re.match("\At[+]\s*[a-zA-Z]+[ ]*[a-zA-Z]*\Z", line):
            name = re.findall("[a-zA-Z ]+", line)[1]
            rgb = self.editor.rainbow.get_rgb_color(*self.editor.last_click)
            print(self.editor.core.add_terrain(name, rgb, 0.0, 0.0))

        elif re.match("\An[+]\s*[a-zA-Z]+[ ]*[a-zA-Z]*\Z", line):
            name = re.findall("[a-zA-Z ]+", line)[1]
            print(self.editor.core.add_nation(name))

        elif re.match("\Ac[+]\s*[a-zA-Z]+[ ]*[a-zA-Z]*\Z", line):
            name = re.findall("[a-zA-Z ]+", line)[1]
            print(self.editor.core.add_control(name))

        elif re.match("\Ag[+]\s*[a-zA-Z]+[ ]*[a-zA-Z]*\Z", line):
            name = re.findall("[a-zA-Z ]+", line)[1]
            print(self.editor.core.add_good(name))

        elif re.match("\As[+]\s*[a-zA-Z]+[ ]*[a-zA-Z]*\Z", line):
            name = re.findall("[a-zA-Z ]+", line)[1]
            print(self.editor.core.add_process(name))

        ###########################################################################
        # sub
        
        elif re.match("\Ap-[0-9]+\Z", line):
            p_id = int(re.findall("[0-9]+", line)[0])
            if self.editor.objects["p"] is self.editor.core.provinces[p_id]:
                self.editor.core.rm_province(p_id)
                self.editor.set_object("p", 0)
                print("rm:", p_id)

        elif re.match("\At-[0-9]+\Z", line):
            t_id = int(re.findall("[0-9]+", line)[0])
            if self.editor.objects["t"] is self.editor.core.terrains[t_id]:
                self.editor.core.rm_terrain(t_id)
                self.editor.set_object("t", 0)
                print("rm:", t_id)

        elif re.match("\An-[0-9]+\Z", line):
            n_id = int(re.findall("[0-9]+", line)[0])
            if self.editor.objects["n"] is self.editor.core.nations[n_id]:
                self.editor.core.rm_nation(n_id)
                self.editor.set_object("n", 0)
                print("rm:", n_id)

        elif re.match("\Ac-[0-9]+\Z", line):
            c_id = int(re.findall("[0-9]+", line)[0])
            if self.editor.objects["c"] is self.editor.core.controls[c_id]:
                self.editor.core.rm_control(c_id)
                self.editor.set_object("c", 0)
                print("rm:", c_id)

        elif re.match("\Ag-[0-9]+\Z", line):
            g_id = int(re.findall("[0-9]+", line)[0])
            if self.editor.objects["g"] is self.editor.core.goods[g_id]:
                self.editor.core.rm_good(g_id)
                self.editor.set_object("g", 0)
                print("rm:", g_id)

        elif re.match("\As-[0-9]+\Z", line):
            s_id = int(re.findall("[0-9]+", line)[0])
            if self.editor.objects["s"] is self.editor.core.processes[s_id]:
                self.editor.core.rm_process(s_id)
                self.editor.set_object("s", 0)
                print("rm:", s_id)
            
        ###########################################################################
        # mod
        
        elif re.match("\At_\s*rgb\Z", line):
            if self.editor.objects["t"]:
                rgb = self.editor.rainbow.get_rgb_color(*self.editor.last_click)
                self.editor.objects["t"].set_rgb(rgb)
                print("mod:", self.editor.objects["t"])
            else: print("not set")
                
        elif re.match("\At_\s*[0-9]+[.]?[0-9]?\s+[0-9]+[.]?[0-9]?\Z", line):
            if self.editor.objects["t"]:
                con_in, con_out = re.findall("[0-9]+[.]?[0-9]?", line)
                self.editor.objects["t"].set_con(float(con_in), float(con_out))
                print("mod:", self.editor.objects["t"])
            else: print("not set")
                
        ###########################################################################
        # pen

        elif re.match("\Ad\Z", line):
            self.editor.objects["d"]+=1
            if self.editor.objects["d"]>=len(self.editor.pens):
                self.editor.objects["d"]-=len(self.editor.pens)
            label = self.editor.pens[self.editor.objects["d"]]
            self.editor.labels["d"].set_text("d:"+label)
            print("pen:", label)
            
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
        # print settings

        elif re.match("\A.rgb\Z", line):
            r,g,b = self.editor.rainbow.get_rgb_color(*self.editor.last_click)
            print("rgb:", r, g, b)

        elif re.match("\A.xy\Z", line):           
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

        else: print("command not matched:", line)
