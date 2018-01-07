import json

class EmpSaver(dict):
    def save_diagram(self, diagram):
        diagram.save(self["params"]["diagram ppm"])            
        
    def __setitem__(self, key, val):        
        if key == "terrains":
            val = val.get_conf()
        elif key == "params":
            pass
        else:
            raise KeyError("%s unexpected key!" % val)
        
        dict.__setitem__(self, key, val)
    
    def save(self, fname):
        if fname[-5:] != ".json" and  fname[-5:] != ".JSON":
            raise ValueError("file %s not looks as JSON" % fname)

        if not "terrains" in self.keys():
            raise KeyError("terrains have to be set")
        if not "params" in self.keys():
            raise KeyError("params have to be set")

        with open(fname, "w") as fd:
            json.dump(self, fd)
        print("(info) save config as:", fname)
