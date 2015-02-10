#!/usr/bin/env python

import sys


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    infile = args[0]
    outfile = '.'.join(infile.split('.')[:-1])

    output = ''
    for line in file(infile):
        if line[0] != '#':
            while line.startswith(' '):
                line = line[1:]
            line = line.replace('"', '%22');
            line = line.replace(' ', '%20');
            output += line.strip()

    file(outfile, 'wb').write(output)
            
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

