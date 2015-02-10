#!/usr/bin/env python

import sys
import os

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    if len(args) < 1:
        infile = sys.stdin
    elif os.path.exists(args[0]):
        infile = file(args[0])
    else:
        import StringIO
        infile = StringIO.StringIO(args[0])

    input = infile.read().strip()

    depth = 0
    output = ''
    for i in range(0, len(input), 2):
        s = input[i:i+2]
        value = int(s, 16)
        char = chr(value)
        output += char
        
    print output
    return 0


if __name__ == '__main__':
    sys.exit(main())

