#!/usr/bin/python3

import sys

class EmpRainbow:

    def __init__(self, width, height):
        if width<2 or height<2:
            sys.stderr.write("width or height < 2")
            sys.exit(-1)

        self.width = width
        self.height = height
        self.rgb = [255, 255, 255]*self.width*self.height

        width2 = self.width/2
        width3 = self.width/3
        height2 = self.height/4
    
        for x in range(self.width):
            if x<width3:
                r = 255.0 - 255.0*float(x)/width3
                g = 255.0*float(x)/width3
                b = 0.0
            elif x<2*width3:
                r = 0.0
                g = 255.0 - 255.0*float(x-width3)/width3
                b = 255.0*float(x-width3)/width3
            else:
                r = 255.0*float(x-2*width3)/width3
                g = 0.0
                b = 255.0 - 255.0*float(x-2*width3)/width3

            for y in range(int(0.75*self.height/2)):
                y+=int(0.25*self.height/2)
                if y<height2:
                    n = float(y)/height2
                    nr, ng, nb = n*r, n*g, n*b
                else:
                    n = float(y-height2)/height2
                    nr = r + float(255.0-r) * n
                    ng = g + float(255.0-g) * n
                    nb = b + float(255.0-b) * n
                
                i = 3 * (x + self.width * y)
                self.rgb[i] = int(nr)
                self.rgb[i+1] = int(ng)
                self.rgb[i+2] = int(nb)

        for x in range(self.width):
            if x<width3:
                r = 255.0 - 255.0*float(x)/width3
                g = 255.0
                b = 255.0*float(x)/width3
            elif x<2*width3:
                r = 255.0*float(x-width3)/width3
                g = 255.0 - 255.0*float(x-width3)/width3
                b = 255.0
            else:
                r = 255.0
                g = 255.0*float(x-2*width3)/width3
                b = 255.0 - 255.0*float(x-2*width3)/width3
                
            for y in range(int(0.75*self.height/2)):
                y+=int(0.25*self.height/2)
                if y<height2:
                    n = float(y)/height2
                    nr, ng, nb = n*r, n*g, n*b
                else:
                    n = float(y-height2)/height2
                    nr = r + float(255.0-r) * n
                    ng = g + float(255.0-g) * n
                    nb = b + float(255.0-b) * n

                i = 3 * (x + self.width * (int(self.height/2) + int(self.height/2) -1 - y))
                self.rgb[i] = int(nr)
                self.rgb[i+1] = int(ng)
                self.rgb[i+2] = int(nb)

                
    # only one sample can be taken
    def get_rgb_color(self, x, y):
        if x<0 or x>=self.width:
            sys.stderr.write("x out of range")
            sys.exit(-1)
        if y<0 or y>=self.height:
            sys.stderr.write("y out of range")
            sys.exit(-1)

        i = 3 * (x + self.width * y)
        return (self.rgb[i], self.rgb[i+1], self.rgb[i+2])
                
