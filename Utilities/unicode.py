#!/usr/bin/env python

import sys

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    input = ''.join(args)
    print input
    return 0


if __name__ == '__main__':
    sys.exit(main())

