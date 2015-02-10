#!/usr/bin/env python

import sys
import os
import re
import glob
import optparse

def run(command):
    return os.popen(command).readlines()


def parseArgs(args):
    optParser = optparse.OptionParser()
    optParser.add_option('-f', action='store', type='string', dest='files',
                         default=None)
    return optParser.parse_args(args)

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    (options, args) = parseArgs(args)

    files = []
    if options.files:
        for line in file(options.files, 'rb'):
            files.append(line.strip())
        
    if len(args) + len(files) < 3:
        print 'pipegrep <pattern> <command (with optional {}s)> <file1> [<file2>...]'
        return 1


    pattern = args[0]

    regexp = re.compile(pattern)    
    command = args[1]
    if -1 == command.find('{}'):
        command += ' {}'
        
    if len(args) > 2:
        files.extend(reduce(lambda x, y: x + y, map(glob.glob, args[2:])))
        
    for f in files:
        lines = [f + ': ' + x.rstrip() for x in run(command.replace('{}', f)) if regexp.search(x) is not None]
        if lines:
            for line in lines:
                print line

    return 0


if __name__ == '__main__':
    sys.exit(main())

