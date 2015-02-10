#!/usr/bin/env python

import os
import sys
import pprint
from optparse import OptionParser

def run(command):
    #logger.debug('about to run "' + command + '" from "' + os.path.abspath(os.curdir) + '"')
    lines = os.popen(command).readlines()
    #logger.debug('ran, and got this: ' + pprint.pformat(lines))
    return lines
    
def sortWithNumerics(items):
    def makeItemToSort(item):
        itemToSort = []
        index = 0
        lookingForNonDigit = True
        while index < len(item):
            chunk = ''
            startIndex = index
            while index < len(item) and (lookingForNonDigit ^ item[index].isdigit()):
                chunk += item[index]
                index += 1
            if len(chunk):
                if not lookingForNonDigit:
                    itemToSort.append(int(chunk))
                else:
                    itemToSort.append(chunk)
            lookingForNonDigit = not lookingForNonDigit
        itemToSort.append(None) # hack to get shorter strings to sort first - without this, a numeric chunk will sort before a string-starting whole item
        itemToSort.append(item)
        return itemToSort
    
    listToSort = [makeItemToSort(x) for x in items]
    listToSort.sort()
    items[:] = [x[-1] for x in listToSort]
    return

def splitOffEndingNumbers(thing):
    firstNumberIndex = len(thing) 
    while firstNumberIndex > 0:
        if thing[firstNumberIndex-1].isdigit():
            firstNumberIndex -= 1
        else:
            break
    return (thing[0:firstNumberIndex], thing[firstNumberIndex:])

def groupRelatedStreams(streamList):
    results = []
    nextGroup = []

    base = None
    for stream in streamList:
        (streamBase, streamNumber) = splitOffEndingNumbers(stream)
        if streamBase != base:
            base = streamBase
            if len(nextGroup) > 0:
                results.append(nextGroup)
                nextGroup = []


        nextGroup.append(stream)

    if len(nextGroup) > 0:
        results.append(nextGroup)
    return results

def formatGroup(group):
    if len(group) == 1:
        return str(group[0])
    else:
        return str(group[0]) + ' - ' + str(group[-1])

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    usage = '\t%prog [options] file'
    parser = OptionParser(usage)
    parser.add_option('--stream', default=None, help='limit to stream')
    (options, args) = parser.parse_args(args)

    if len(args) == 0:
        parser.error('no file supplied')
    
    versionMap = {}

    command = 'cvs -f -q log -h '
    if options.stream:
        goodStream = lambda x: len(x.split('_')) > 2 and x.split('_')[-2] == options.stream
    else:
        goodStream = lambda x: True

    for line in run(command + '"' + args[0] + '"'):
        if line[0].isspace() and -1 != line.find(':'):
            (oneStream, version) = line.split(':')
            # get rid of empty branches
            if '0' in version.split('.'):
                continue
            if -1 != version.find('.') and goodStream(oneStream):
                streamsSoFar = versionMap.get(version.strip(), [])
                streamsSoFar.append(oneStream.strip())
                versionMap[version.strip()] = streamsSoFar

    versions = versionMap.keys()
    sortWithNumerics(versions)

    for version in versions:
        streams = versionMap[version]
        
        sortWithNumerics(streams)
        numComponents = len(version.split('.'))
        version = '' * (numComponents - 2)  + version
        groups = groupRelatedStreams(streams)

        print version, '\t', formatGroup(groups[0])
        for g in groups[1:]:
            print ' ' * len(version), '\t', formatGroup(g)
            
        #else:
        # print version, tags[0], '-', tags[-1]

    return 0


if __name__ == '__main__':
    sys.exit(main())

