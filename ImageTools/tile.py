#!/usr/bin/env python

import sys
import Image
import optparse
import glob


def usage():
    print 'usage:', sys.argv[0], '[<rows>x<columns>] image1 image2 ...'
    print 'example:', sys.argv[0], '1x2 image1.jpg image2.jpg'
    print 'all images must be the same dimensions'


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    usage_string = '%prog [options] <rows>x<columns> image1 image2 ...'
    parser = optparse.OptionParser(usage_string)
    parser.add_option('--output', action="store", type="string")
    parser.add_option('--mode', action="store", type="string")
    (options, args) = parser.parse_args(args)

    layout = args.pop(0)
    num_rows, num_columns = [int(x) for x in layout.split('x')]
    num_images = num_rows * num_columns

    filenames = []
    for arg in args:
        filenames.extend(glob.glob(arg))

    if len(filenames) != num_images:
        print 'need', num_images, 'images, but got', len(filenames)
        usage()
        return 1

    images = []
    for filename in filenames:
        images.append(Image.open(filename))

    mode = options.mode or images[0].mode
    width = images[0].size[0]
    height = images[0].size[1]
    output_image = Image.new(mode, (width * num_columns, height * num_rows))

    count = 0
    for i in range(num_columns):
        for j in range(num_rows):
            try:
                output_image.paste(images[count], (width*i, height*j, width*(i+1), height*(j+1)))
            except:
                print 'problem pasting', filenames[count]
                usage()
                return 2
            count += 1

    if options.output:
        output_image.save(options.output)
    else:
        output_image.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
