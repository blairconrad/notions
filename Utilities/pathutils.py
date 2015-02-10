#!/usr/bin/env python

import os

def findDirInParents(target, startingDir):
    '''Find the requested file in this directory or the first
    parent directory that has it'''
    oldStartingDir = ''
    startingDir = os.path.abspath(startingDir)
    while startingDir != oldStartingDir:
        nextGuess = os.path.join(startingDir, target)
        
        if os.path.exists(nextGuess):
            return nextGuess

        oldStartingDir = startingDir
        startingDir = os.path.split(startingDir)[0]
    return None



