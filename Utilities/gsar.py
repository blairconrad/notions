#!/usr/bin/env python

import sys
from optparse import OptionParser
import re
import shutil
import glob

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    parser = OptionParser()
    parser.add_option('-i', action='store_true', dest='insensitive', default=False,
                      help='compare case-insensitively')

    (options, args) = parser.parse_args(args)

    compileFlags = re.MULTILINE # 0 means no flags

    if options.insensitive:
        compileFlags |= re.IGNORECASE
        
    sourceRegexp = re.compile(args.pop(0), compileFlags)
    replacementString = args.pop(0)

    files = []
    for f in args:
        files.extend(glob.glob(f))
        
    for f in files:
        (result, count) = sourceRegexp.subn(replacementString, file(f, 'rb').read())
        if count > 0:
            shutil.move(f, f + '.bak')
            file(f, 'wb').write(result)
    return 0


if __name__ == '__main__':

    
    sys.exit(main())

