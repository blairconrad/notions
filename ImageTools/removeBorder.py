#!/usr/bin/env python

import sys
import Image


def croppedSize(thickness, size):
    return (thickness, thickness, size[0] - thickness, size[1] - thickness)

def main(args=None):
    if args == None:
        args = sys.argv[1:]
    if len(args) == 0:
        print sys.argv[0], "<thickness> <infile> [<outfile>]"
        return 0

    thickness = int(args[0])
    infile = args[1]

    i = Image.open(infile)
    cropped = i.crop(croppedSize(thickness, i.size))

    if len(args) > 2:
        cropped.save(args[2])
    else:
        cropped.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())

