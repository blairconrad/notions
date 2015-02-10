#!/usr/bin/env python

import sys
import os
import tempfile

CVS_UPDATE_COMMAND = 'cvs -f -q update -p ' 

def run(command):
    return os.popen(command).read()


def cleanFileName(fn):
    return fn.replace('/', '_').replace('\\', '_')

def doDiff(record):
    if record.oldRevision:
        command = CVS_UPDATE_COMMAND + record.oldFlag + ' ' + record.oldRevision
        prefix = cleanFileName(record.fileName) + '_' + record.oldRevision
    else:
        command = CVS_UPDATE_COMMAND
        prefix = cleanFileName(record.fileName)
    contents = run(command + ' "' + record.fileName + '"')
    
    (fd, oldTempFileName) = tempfile.mkstemp(suffix=prefix)
    f = os.fdopen(fd, 'w+b')
    f.write(contents)
    f.close()

    if record.newRevision:
        command = CVS_UPDATE_COMMAND + record.newFlag + ' ' + record.newRevision
        contents = run(command + ' "' + record.fileName + '"')
        (fd, newTempFileName) = tempfile.mkstemp(suffix=cleanFileName(record.fileName) + '_' + record.newRevision)
        f = os.fdopen(fd, 'w+b')
        f.write(contents)
        f.close()
    else:
        newTempFileName = record.fileName

    
    
    print oldTempFileName, newTempFileName
    run('compare "' + oldTempFileName + '" "' + newTempFileName + '"')

class diffRecord:
    def __init__(self):
        self.fileName = None
        self.oldFlag = None
        self.oldRevision = None
        self.newFlag = None
        self.newRevision = None

def main(args=None):
    if args == None:
        args = sys.argv[1:]


    if len(args) == 0:
        print 'cvsadiff [-r rev1.a [-r rev2.a]] file.a [[-r rev1.b [-r rev2.b]] file.b] ...'

    nextModifier = None
    nextRecord = diffRecord()
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ['-r', '-D']:
            flag = arg
            i += 1
            arg = args[i]
            
            if nextRecord.oldRevision:
                nextRecord.newFlag = flag
                nextRecord.newRevision = arg
            else:
                nextRecord.oldFlag = flag
                nextRecord.oldRevision = arg

        elif arg.find('-r') == 0 or arg.find('-D') == 0:
            flag = arg[:2]
            arg = arg[2:]            
            if nextRecord.oldRevision:
                nextRecord.newFlag = flag
                nextRecord.newRevision = arg
            else:
                nextRecord.oldFlag = flag
                nextRecord.oldRevision = arg
        else:
            #filename
            nextRecord.fileName = arg
            doDiff(nextRecord)
            nextModifier = None
            nextRecord = diffRecord()
        i += 1

if __name__ == '__main__':
    sys.exit(main())

