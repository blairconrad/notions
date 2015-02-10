#!/usr/bin/env python

import sys

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    input = file(args[0], 'r').read()
    utf8 = unicode(input, 'utf-8')
    print map(ord, utf8)

    u = utf8.encode('utf-16')
    print map(ord, u)

    file('unicode.txt', 'w').write(u)

    return 0


if __name__ == '__main__':
    sys.exit(main())

