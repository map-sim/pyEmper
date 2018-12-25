#! /usr/bin/python3
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import sys
from termcolor import colored

debug = True

def printInfo(info):
    prefix = colored("(info)", "green")
    out = "%s %s\n" % (prefix, info)
    sys.stdout.write(out)

def printError(info):
    prefix = colored("(error)", "red")
    out = "%s %s\n" % (prefix, info)
    sys.stderr.write(out)

def printWarning(info):
    prefix = colored("(warning)", "yellow")
    out = "%s %s\n" % (prefix, info)
    sys.stderr.write(out)

def printDebug(info):
    if not debug:
        return
    
    prefix = colored("(debug)", "cyan")
    out = "%s %s\n" % (prefix, info)
    sys.stderr.write(out)

def str2rgb(strrgb):
    r = int(strrgb[0:2], 16)
    g = int(strrgb[2:4], 16)
    b = int(strrgb[4:], 16)
    return r, g, b

def rgb2str(rgb):
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def findMax(buff, node):
    maxNode = None
    maxInt = 0
    
    for n in buff.key():
        if buff[n] > maxInt:
            maxInt = buff[n] 
            maxNode = n
            
        elif buff[n] == maxInt and n==node:
            maxInt = buff[n] 
            maxNode = n

    return maxNode
