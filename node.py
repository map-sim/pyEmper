#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


class EmpNode(set):
    def __init__(self, conf):
        self.name = conf["name"]
        set.__init__(self)
        self.conf = conf

    def get_config(self):
        return self.conf

