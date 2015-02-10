#!/usr/bin/env/python

import os
import stat
import sys
import shutil
import subprocess

moveToDir = r'D:\bconrad\Documents\DropBox\My Dropbox\Audio\Queued PodCasts'

def move(fileToPlay):
    currentDir = os.path.split(os.path.abspath(fileToPlay))[0]
    if currentDir != moveToDir:
        os.chmod(fileToPlay, stat.S_IRWXU)
        shutil.move(fileToPlay, moveToDir)
    newLocation = os.path.join(moveToDir, os.path.split(fileToPlay)[1])
    print newLocation
    return newLocation

def play(fileToPlay):
    foobar = r'd:\bconrad\PortableApps\Foobar 2000\foobar2000.exe'
    subprocess.call([foobar, '/add', fileToPlay])


def main(args=None):
    if args == None:
        args = sys.argv[1:]
	
    fileToPlay = ' '.join(args)
    try:
        newFileLocation = move(fileToPlay)
        #play(newFileLocation)
    except Exception, e:
        #f = file(r'c:\play.log', 'wb')
        #f.write(str(e))
        #f.close()
        raise e
        
    
if __name__ == '__main__':
	 sys.exit(main())
