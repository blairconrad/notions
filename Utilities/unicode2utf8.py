#!/usr/bin/env python

import sys

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    input = file(args[0], 'r').read()
    u = unicode(input, 'utf-16')
    print map(ord, u)

    utf8 = u.encode('utf-8')
    print map(ord, utf8)

    file('utf8.txt', 'w').write(utf8)

    return 0


if __name__ == '__main__':
    sys.exit(main())

