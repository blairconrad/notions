#!/usr/bin/env python

from __future__ import print_function
import sys
import glob
import os.path
import re
import optparse
import fnmatch

"""A module that performs recursive searches for strings"""


def open_file(filename):
    if filename == "-":
        return sys.stdin
    else:
        return open(filename, encoding="utf8")


def check_file(regexp, filename):
    try:
        print("opening", filename)
        f = open_file(filename)
    except IOError as detail:
        sys.stderr.write("error: unable to open " + filename + " for reading: " + detail.strerror + "\n")
        return

    try:
        for line in f.readlines():
            if regexp.search(line) is not None:
                print(filename)
                f.close()
                return
    except UnicodeDecodeError:
        pass


def print_lines(regexp, filename):
    global options
    try:
        f = open_file(filename)
        i = 0
        for line in f.readlines():
            i += 1
            if regexp.search(line) is not None:
                if options.emacsLineNumbers:
                    print("+%d %s %s" % (i, filename, line.rstrip()))
                else:
                    print("%s:%d:%s" % (filename, i, line.rstrip()))
    except IOError as detail:
        sys.stderr.write("error: unable to open " + filename + " for reading: " + detail.strerror + "\n")
        return
    except UnicodeDecodeError:
        pass
    f.close()


def add_files(fringe, dirname, names):
    global options
    for name in names:
        fullname = os.path.join(dirname, name)
        if not os.path.isdir(fullname):
            fringe.append(os.path.normpath(fullname))


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    global options

    usage = "%prog [options] <regexp> <path>+"
    option_parser = optparse.OptionParser(usage)
    option_parser.add_option(
        "-i",
        "--ignore-case",
        action="store_true",
        dest="ignoreCase",
        default=False,
        help="ignore case when matching patterns",
    )
    option_parser.add_option(
        "-l",
        "--list-files",
        action="store_true",
        dest="listFiles",
        default=False,
        help="print only name of files with matching lines",
    )
    option_parser.add_option(
        "--include-files",
        metavar="PATTERN",
        action="store",
        dest="includeFiles",
        help="only examine files whose names match PATTERN",
    )
    option_parser.add_option(
        "-e",
        "--emacs",
        action="store_true",
        dest="emacsLineNumbers",
        default=False,
        help="render line numbers for opening in emacs",
    )

    (options, args) = option_parser.parse_args(args)

    regexp_flags = 0

    if options.ignoreCase:
        regexp_flags |= re.IGNORECASE

    if options.listFiles:
        file_checker = check_file
    else:
        file_checker = print_lines

    regexp = None

    pattern = args[0]
    regexp = re.compile(pattern, regexp_flags)

    fringe = []

    # Suck in all the files and directories to check
    if len(args) < 2:
        args.append(".")

    for filespec in args[1:]:
        globbed_roots = glob.glob(filespec)
        if len(globbed_roots) == 0:
            if filespec == "-":
                globbed_roots = ["-"]
            else:
                print("No files match argument '%s'. Quitting." % (filespec,))
                return 1

        for root in globbed_roots:
            if os.path.isdir(root):
                for (dirpath, dirnames, filenames) in os.walk(root):
                    add_files(fringe, dirpath, filenames)
            else:
                fringe.append(root)

    # Process the directories
    for filepath in fringe:
        filename = os.path.split(filepath)[1]
        if not options.includeFiles or fnmatch.fnmatch(filename, options.includeFiles):
            file_checker(regexp, filepath)

    return 0


if __name__ == "__main__":
    sys.exit(main())
