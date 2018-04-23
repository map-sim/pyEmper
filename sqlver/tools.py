#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

import os
import sys
from termcolor import colored

def print_error(info):
    prefix = colored("(error)", "red")
    out = "%s %s\n" % (prefix, info)
    sys.stderr.write(out)

def print_info(info):
    prefix = colored("(info)", "green")
    out = "%s %s\n" % (prefix, info)
    sys.stderr.write(out)

def str_to_rgb(strrgb):
    r = int(strrgb[0:2], 16)
    g = int(strrgb[2:4], 16)
    b = int(strrgb[4:], 16)
    return r, g, b

def xy_gener(width, height):
    for y in range(height):
        for x in range(width):
            yield x, y
            
def sub_rgb(rgb1, rgb2):
    out = 0
    for i, j in zip(rgb1, rgb2):
        out += abs(i - j)
    return out

def get_nearest_rgb(palette, rgb):
    print(palette, rgb)
    
    tmp = [(sub_rgb(t, rgb), t) for t in palette]
    tmp = min(tmp, key=lambda e: e[0])
    return tmp[1]

def readline(fd):
    line = fd.readline()
    while "#" in line:
        line = fd.readline()
    return line

def rgb_reader(fd):
    index = 0
    while True:
        try:
            r = int(readline(fd))
            g = int(readline(fd))
            b = int(readline(fd))
            yield index, (r, g, b)
            index += 1
        except ValueError:
            break
    fd.close()

def ppm_loader(fname):
    
    if not os.path.exists(fname):
        raise ValueError("file %s not exists" % fname)
    if fname[-4:] != ".ppm" and  fname[-4:] != ".PPM":
        raise ValueError("file %s not looks as PPM" % fname)

    fd = open(fname, "r")
    line = readline(fd) 
    if line[0:2] != "P3":
        raise ValueError("file %s not looks as P3" % fname)
    
    width, height = readline(fd).split()
    width, height = int(width), int(height)
    deep = readline(fd)

    return width, height, rgb_reader(fd)
