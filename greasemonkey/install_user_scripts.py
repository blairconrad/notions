#!/usr/bin/env python

import sys
from suck_back_user_scripts import *

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    gmPath = getGmPath();

    for fileToCopy in filesToCopy:
        sourceFile = fileToCopy[THISDIR]
        destFile = os.path.join(gmPath, fileToCopy[GMDIR])
        copyFile(sourceFile, destFile)

    return 0

if __name__ == '__main__':
    sys.exit(main())

