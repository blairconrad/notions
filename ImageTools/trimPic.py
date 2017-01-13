#!/usr/bin/env python

import sys
import Image


def trim(im):

    background_colour = im.getpixel((0, 0))

    # work along the left edge of the picture
    left = -1
    right = -1
    top = -1
    bottom = -1

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            colour = im.getpixel((i, j))
            if colour != background_colour:
                left = i
                break
        if left != -1:
            break

    if left == -1:
        return im

    for i in range(im.size[1]):
        for j in range(left, im.size[0]):
            colour = im.getpixel((j, i))
            if colour != background_colour:
                top = i
                break
        if top != -1:
            break

    for i in range(im.size[1]-1, top-1, -1):
        for j in range(left, im.size[0]):
            colour = im.getpixel((j, i))
            if colour != background_colour:
                bottom = i+1
                break
        if bottom != -1:
            break

    for i in range(im.size[0]-1, left-1, -1):
        for j in range(top, bottom):
            colour = im.getpixel((i, j))
            if colour != background_colour:
                right = i+1
                break
        if right != -1:
            break

    print 'left =', left
    print 'right =', right

    print 'top =', top
    print 'bottom =', bottom

    cropped = im.crop((left, top, right, bottom))
    return cropped


def main(args=None):
    if args is None:
        args = sys.argv

    file_to_trim = args[1]
    im = Image.open(file_to_trim)
    print im.size

    cropped = trim(im)
    print cropped.size

    if len(args) > 2:
        cropped.save(args[2])
    else:
        cropped.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
