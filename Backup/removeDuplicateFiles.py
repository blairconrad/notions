#!/usr/bin/env python

# Set up the logger
import logging
logger = logging.getLogger('backup.removeDuplicates')

import sys
import os
import filecmp

def cleanDir(dir):
    fileNames = os.listdir(dir)
    fileNames.sort()

    lastFileChecked = os.path.join(dir, fileNames[0])
    for fileName in fileNames[1:]:
        fileName = os.path.join(dir, fileName)
        #print 'comparing', lastFileChecked, fileName
        if filecmp.cmp(lastFileChecked, fileName, shallow=0):
            # remove the new one
            #print 'removing', fileName
            os.unlink(fileName)
        else:
            lastFileChecked = fileName
    return 0


if __name__ == '__main__':
    sys.exit(cleanDir(sys.argv[1]))

