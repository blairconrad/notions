#!/usr/bin/env python

import sys
import os.path
import ImageGrab


def make_unique_file_name():
    base_name = 'snap'
    extension = '.png'
    i = 0
    while True:
        distinguisher = '%04d' % i
        file_name = base_name + distinguisher + extension
        if not os.path.exists(file_name):
            return file_name
        i += 1


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    if len(args) > 0:
        out_file_name = args[0]
    else:
        out_file_name = make_unique_file_name()

    ImageGrab.grab().save(out_file_name)

    print 'saved as', out_file_name
    return 0


if __name__ == '__main__':
    sys.exit(main())
