#!/usr/bin/env python

import sys
import os.path
import ImageGrab

def makeUniqueFileName():
    baseName = 'snap'
    extension = '.png'
    i = 0
    while True:
        distinguisher = '%04d' % i
        fileName = baseName + distinguisher + extension
        if not os.path.exists(fileName):
            return fileName
        i += 1

def main(args=None):
    if args == None:
        args = sys.argv[1:]

        
    if len(args) > 0:
        outFileName = args[0]
    else:
        outFileName = makeUniqueFileName()

    ImageGrab.grab().save(outFileName)

    print 'saved as', outFileName
    return 0


if __name__ == '__main__':
    sys.exit(main())

