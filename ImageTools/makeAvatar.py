#!/usr/bin/env python

import sys
import Image
import optparse
import trimPic

def squareIt(im, backgroundColour):
    if im.size[0] < im.size[1]:
        newIm = Image.new(im.mode, (im.size[1], im.size[1]), backgroundColour)
        newIm.paste(im, ((im.size[1] - im.size[0])/2, 0))
        return newIm
    elif im.size[0] > im.size[1]:
        newIm = Image.new(im.mode, (im.size[0], im.size[0]), backgroundColour)
        newIm.paste(im, (0, (im.size[0] - im.size[1])/2))
        return newIm
    else:
        return im

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    parser = optparse.OptionParser()
    parser.add_option('--size', action="store", type="int", default=96)
    parser.add_option('--margin', action="store", type="int", default=0)
    parser.add_option('--trim', action="store_true", dest="trim", default=False)
    parser.add_option('--background', action="store", type="string", dest="background", default=None)

    (options, args) = parser.parse_args(args)

    fileToTrim = args[0]
    if len(args) > 1:
        outputFile = args[1]
    else:
        outputFile = None

    # There was a .convert('RGB') here, and I don't know why.  It
    # messed up resizing PNGs with Alpha Channels, so I got rid of it.
    im = Image.open(fileToTrim)
    print 'original size =', im.size

    if options.trim:
        im = trimPic.trim(im)
        print 'cropped size =', im.size

    # figure out desired size - only works for squares for now
    desiredFinalSize = (options.size, options.size)
    desiredPictureSize = (desiredFinalSize[0] - 2 * options.margin, desiredFinalSize[1] - 2 * options.margin)
    
    background = options.background
    if not background:
        background = im.getpixel((0,0))

    squared = squareIt(im, background)
    print 'squared size =', squared.size

    resized = squared.resize(desiredPictureSize, Image.ANTIALIAS)

    print 'resized size =', resized.size
    
    #resized = squareIt(resized)
    #print 'squared resized size =', resized.size

    print 'top-left pixel colour =', resized.getpixel((0,0))
    newPic = Image.new(resized.mode, desiredFinalSize, resized.getpixel((0,0)))
    newPic.paste(resized, (options.margin, options.margin))
    print 'new size = ', newPic.size

    if outputFile:
        newPic.save(outputFile)
    else:
        newPic.show()


    return 0


if __name__ == '__main__':
    sys.exit(main())

