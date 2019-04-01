#!/usr/bin/env python

from __future__ import print_function
import sys
import glob
import os.path
import re
import optparse
import fnmatch

'''A module that performs recursive searches for strings'''


def open_file(filename):
    if filename == '-':
        return sys.stdin
    else:
        return open(filename)


def checkFile(regexp, filename):
    try:
        f = open_file(filename)
    except IOError as detail:
        sys.stderr.write('error: unable to open ' + filename +
                         ' for reading: ' + detail.strerror + '\n')
        return

    for line in f.readlines():
        if regexp.search(line) is not None:
            print(filename)
            f.close()
            return


def printLines(regexp, filename):
    global options
    try:
        f = open_file(filename)
    except IOError as detail:
        sys.stderr.write('error: unable to open ' + filename +
                         ' for reading: ' + detail.strerror + '\n')
        return

    i = 0
    for line in f.readlines():
        i += 1
        if regexp.search(line) is not None:
            if options.emacsLineNumbers:
                print('+%d %s %s' % (i, filename, line.rstrip()))
            else:
                print('%s:%d:%s' % (filename, i, line.rstrip()))
    f.close()


def addFiles(fringe, dirname, names):
    global options
    for name in names:
        fullname = os.path.join(dirname, name)
        if not os.path.isdir(fullname):
            fringe.append(os.path.normpath(fullname))


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    global options

    usage = '%prog [options] <regexp> <path>+'
    optParser = optparse.OptionParser(usage)
    optParser.add_option('-i', '--ignore-case', action='store_true', dest='ignoreCase', default=False,
                         help='ignore case when matching patterns')
    optParser.add_option('-l', '--list-files', action='store_true', dest='listFiles', default=False,
                         help='print only name of files with matching lines')
    optParser.add_option('--include-files', metavar='PATTERN', action='store', dest='includeFiles',
                         help='only examine files whose names match PATTERN')
    optParser.add_option('-e', '--emacs',  action='store_true', dest='emacsLineNumbers', default=False,
                         help='render line numbers for opening in emacs')

    (options, args) = optParser.parse_args(args)

    regexpFlags = 0

    if options.ignoreCase:
        regexpFlags |= re.IGNORECASE

    if options.listFiles:
        fileChecker = checkFile
    else:
        fileChecker = printLines

    regexp = None

    pattern = args[0]
    regexp = re.compile(pattern, regexpFlags)

    fringe = []

    # Suck in all the files and directories to check
    if len(args) < 2:
        args.append('.')

    for filespec in args[1:]:
        globbedRoots = glob.glob(filespec)
        if len(globbedRoots) == 0:
            if filespec == '-':
                globbedRoots = ['-']
            else:
                print("No files match argument '%s'. Quitting." % (filespec,))
                return 1

        for root in globbedRoots:
            if os.path.isdir(root):
                for (dirpath, dirnames, filenames) in os.walk(root):
                    addFiles(fringe, dirpath, filenames)
            else:
                fringe.append(root)

    # Process the directories
    for filepath in fringe:
        filename = os.path.split(filepath)[1]
        if not options.includeFiles or fnmatch.fnmatch(filename, options.includeFiles):
            fileChecker(regexp, filepath)

    return 0


if __name__ == '__main__':
    sys.exit(main())
