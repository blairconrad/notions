#!/usr/bin/env python

import sys
import Image
import ImageChops
import ImageStat
import math

def main(args=None):
    if args == None:
        args = sys.argv

    i1 = Image.open(args[1])
    i2 = Image.open(args[2])
    diff = ImageChops.difference(i1,i2)

    stats = ImageStat.Stat(diff)
    maxDiff = max(stats.extrema[0][1], stats.extrema[1][1], stats.extrema[2][1])


    if 0 == maxDiff:
        print 'no difference'
        return 0
    
    scaleFactor = 191.0 / math.sqrt(maxDiff)
    print maxDiff,scaleFactor

    def transFormBand(bandValue):
        if bandValue != 0:
            bandValue = 64 + int(scaleFactor * math.sqrt(bandValue))
        return bandValue

    diff = Image.eval(diff, transFormBand)
    diff.show()

    if len(args) > 3:
        diff.save(args[3])
    return 0


if __name__ == '__main__':
    sys.exit(main())

