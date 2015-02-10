#!/usr/bin/env python

import sys
import os
import glob
import optparse
import pathutils

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    parser = optparse.OptionParser()
    parser.add_option('--out', dest='out', default=None)
    parser.add_option('--fixture', dest='fixture', default=None)
    parser.add_option('--include', dest='include', default=None)
    parser.add_option('--exclude', dest='exclude', default=None)
    (options, args) = parser.parse_args()
    
    nunit = pathutils.findDirInParents('outputs\\intermediates\\bin\\win32\\nunit-console.exe', os.getcwd())

    things = []
    for arg in args:
        newThings = glob.glob(arg)
        if len(newThings) == 0:
            print arg, 'does not resolve to any file system object. Aborting.'
            return -1
        things.extend(newThings)

    if len(things) == 0:
        print 'No unit tests specified. Aborting.'
        return -2
    
    extraOpts = ['/labels']
    if options.out:
        extraOpts += ['/out', options.out]
    if options.fixture:
        extraOpts += ['/fixture=' + options.fixture]
    if options.include:
        extraOpts += ['/include=' + options.include]
    if options.exclude:
        extraOpts += ['/exclude=' + options.exclude]

    for thing in things:
        print 'Testing', thing
        if os.path.isdir(thing):
            thing = thing + '\\bin\\Release\\' + thing + '.dll'

        if os.path.isfile(thing):
            os.spawnv(os.P_WAIT, nunit, ['nunit'] + extraOpts + [thing])
        else:
            print thing, 'is neither a directory nor a file. Aborting.'
            return -3
            
    return 0

if __name__ == '__main__':
    sys.exit(main())

