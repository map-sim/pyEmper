#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


import os


def readline(fd):
    line = fd.readline()
    while "#" in line:
        line = fd.readline()
    return line


def RGBreader(fd):
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

    
def PPMloader(fname):
    
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

    return width, height, RGBreader(fd)
