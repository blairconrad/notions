#!/usr/bin/env python

import sys
import Image
import optparse
import trimPic


def square_it(im, background_colour):
    if im.size[0] < im.size[1]:
        new_im = Image.new(im.mode, (im.size[1], im.size[1]), background_colour)
        new_im.paste(im, ((im.size[1] - im.size[0])/2, 0))
        return new_im
    elif im.size[0] > im.size[1]:
        new_im = Image.new(im.mode, (im.size[0], im.size[0]), background_colour)
        new_im.paste(im, (0, (im.size[0] - im.size[1])/2))
        return new_im
    else:
        return im


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = optparse.OptionParser()
    parser.add_option('--size', action="store", type="int", default=96)
    parser.add_option('--margin', action="store", type="int", default=0)
    parser.add_option('--trim', action="store_true", dest="trim", default=False)
    parser.add_option('--background', action="store", type="string", dest="background", default=None)

    (options, args) = parser.parse_args(args)

    file_to_trim = args[0]
    if len(args) > 1:
        output_file = args[1]
    else:
        output_file = None

    # There was a .convert('RGB') here, and I don't know why.  It
    # messed up resizing PNGs with Alpha Channels, so I got rid of it.
    im = Image.open(file_to_trim)
    print 'original size =', im.size

    if options.trim:
        im = trimPic.trim(im)
        print 'cropped size =', im.size

    # figure out desired size - only works for squares for now
    desired_final_size = (options.size, options.size)
    desired_picture_size = (desired_final_size[0] - 2 * options.margin, desired_final_size[1] - 2 * options.margin)

    background = options.background
    if not background:
        background = im.getpixel((0, 0))

    squared = square_it(im, background)
    print 'squared size =', squared.size

    resized = squared.resize(desired_picture_size, Image.ANTIALIAS)

    print 'resized size =', resized.size

    print 'top-left pixel colour =', resized.getpixel((0, 0))
    new_pic = Image.new(resized.mode, desired_final_size, resized.getpixel((0, 0)))
    new_pic.paste(resized, (options.margin, options.margin))
    print 'new size = ', new_pic.size

    if output_file:
        new_pic.save(output_file)
    else:
        new_pic.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
