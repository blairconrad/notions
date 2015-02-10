#!/usr/bin/env python

import sys
import os

def run(command):
    return os.popen(command).read()

def main(args=None):
    if args == None:
        args = sys.argv[1:]
    inLines = map(str.strip, file(args[0], 'rb').readlines())
    i = 0
    while i < len(inLines):
        line = inLines[i]
        if len(line) > 0 and len(line)-1 == line.find(';'):
            fileName = line.strip()[:-1]
            #print fileName
            i += 1
            line = inLines[i]
            tokens = line.split()
            newRevision = tokens[2].replace(';', '')
            oldRevision = tokens[5]
            #print oldRevision, newRevision
            run('cvsadiff -r ' + oldRevision + ' -r ' + newRevision + ' ' + fileName)
        i += 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

