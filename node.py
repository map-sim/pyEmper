#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


class EmpNode:
    def __init__(self, conf):
        self.conf = conf

    def get_config(self):
        return self.conf
