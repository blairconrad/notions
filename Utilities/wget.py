#!/usr/bin/env python

import sys
import urllib2

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    for url in args:
        outputFilename = url.split('/')[-1]
        print 'reading', url, 'to store in', outputFilename
        source = urllib2.urlopen(args[0])

        outputFile = open(outputFilename, 'wb')

        totalBytes = 0
        data = source.read(8192)
        while data:
            totalBytes += len(data)
            outputFile.write(data)
            data = source.read(8192)

        outputFile.close()
        print 'wrote', totalBytes, 'bytes to', outputFilename
        return 0



if __name__ == '__main__':
    sys.exit(main())

