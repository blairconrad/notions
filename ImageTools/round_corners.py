#!/usr/bin/env python

import sys
import Image
import math

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    radius = 10

    white = (255,255,255)
    image = Image.open(args[0])
    for i in range(radius):
        for j in range(radius):
            if ((radius - i)*(radius - i) + (radius - j)*(radius - j)) > radius*radius:
                image.putpixel((i,j), white)
                image.putpixel((image.size[0]-1-i,j), white)
                image.putpixel((i,image.size[1]-1-j), white)
                image.putpixel((image.size[0]-1-i,image.size[1]-1-j), white)
                
    if len(args) > 1:
        image.save(args[1])
    else:
        image.show()
    return 0


if __name__ == '__main__':
    sys.exit(main())

