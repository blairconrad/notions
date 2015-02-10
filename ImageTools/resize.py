#!/usr/bin/env python

import sys
import Image


def main(args=None):
    if args == None:
        args = sys.argv[1:]
    if len(args) == 0:
        print sys.argv[0], "<scale percentage> <infile> [<outfile>]"
        return 0

    scale = float(args[0])/100.0
    infile = args[1]

    i = Image.open(infile)
    newSize = (int(i.size[0] * scale), int(i.size[1] * scale))

    resized = i.resize(newSize, Image.ANTIALIAS)
    
    if len(args) > 2:
        resized.save(args[2])
    else:
        resized.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())

