#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

import time
from termcolor import colored


def measure_time(info):
    def decorate_func(func):
        def get_args(*args, **kwargs):
            tmp = time.time() 
            ret = func(*args, **kwargs)
            print(colored("* %s in %.2f s" % (info, time.time() - tmp), "green"))
            return ret
        return get_args
    return decorate_func


def xy_gen(scale, w, h=None):
    if not h is None:
        for y in range(h):
            for sy in range(scale):
                for x in range(w):
                    for sx in range(scale):                    
                        yield x,y
    elif isinstance(w, (set, list, tuple)):
        for a in w:
            for sy in range(scale):
                for sx in range(scale):                    
                    yield scale*a.x+sx, scale*a.y+sy
