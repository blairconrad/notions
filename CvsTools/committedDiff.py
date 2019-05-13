#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import cvsadiff
import diffSand


def run(command):
    return os.popen(command).read()


def main(args=None):
    if args == None:
        args = sys.argv[1:]

    s = sys.stdin.read()
    lines = [l.strip() for l in s.splitlines()]

    i = 0
    while i < len(lines):
        if lines[i].find("revision:") != -1:
            line = lines[i - 1]
            line = line.replace("/usr/Master/mitra-dev/src/", "")
            commaIndex = line.find(",")
            if commaIndex == -1:
                fileName = line
            else:
                fileName = line[:commaIndex].strip()

            line = lines[i]
            if line.find("previous revision:") == -1:
                diffSand.compareNewFile(fileName)
            else:
                newVersion, sep, prevVersion = line.partition(";")
                newVersion = newVersion.partition(":")[2].strip()
                prevVersion = prevVersion.partition(":")[2].strip()

                record = cvsadiff.diffRecord()
                record.fileName = fileName
                record.oldFlag = "-r"
                record.oldRevision = prevVersion
                record.newFlag = "-r"
                record.newRevision = newVersion

                print("diffing", prevVersion, newVersion, "of", fileName)
                cvsadiff.doDiff(record)
        i += 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
