#!/usr/bin/env python

import sys
import Image


def main(args=None):
    if args is None:
        args = sys.argv

    im = Image.open(args[1])

    zoom_factor = 3

    new_im = Image.new(im.mode, (im.size[0] * zoom_factor, im.size[1] * zoom_factor))
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            pixel = im.getpixel((i, j))
            for k in range(zoom_factor * i, zoom_factor * (i + 1)):
                for l in range(zoom_factor * j, zoom_factor * (j + 1)):
                    new_im.putpixel((k, l), pixel)

    if len(args) > 2:
        new_im.save(args[2])
    else:
        new_im.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
