#!/usr/bin/env python

import sys
import Image

def main(args=None):
    if args == None:
        args = sys.argv

    im = Image.open(args[1])

    zoomFactor = 3

    newIm = Image.new(im.mode, (im.size[0] * zoomFactor, im.size[1] * zoomFactor))
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            pixel = im.getpixel((i,j))
            for k in range(zoomFactor * i, zoomFactor * (i + 1)):
                for l in range(zoomFactor * j, zoomFactor * (j + 1)):
                    newIm.putpixel((k,l), pixel)

    if len(args) > 2:
        newIm.save(args[2])
    else:
        newIm.show()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

