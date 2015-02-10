#!/usr/bin/env python

# Set up the logger
import logging
logger = logging.getLogger('backup.backup')

import pprint
import sys
import zipfile
import os
from fnmatch import fnmatch

class DirectoryBackupper:
    def __init__(self, outputFileName):
        self.outputFileName = os.path.abspath(outputFileName)
        self.workingDirectory = os.curdir

        self.zipfile = zipfile.ZipFile(self.outputFileName,
                                       mode='w',
                                       compression=zipfile.ZIP_DEFLATED)

    def ignoreFileList(self, root, dirs, files, ignoreFiles):
        # TODO: add error handling in case can't open the ignoreFiles file
        thingsToIgnore = []
        if type(ignoreFiles) == type(''):
            if ignoreFiles in files:
                for line in open(os.path.join(root, ignoreFiles)).readlines():
                    thingsToIgnore.append(line.strip())
        else:
            thingsToIgnore = ignoreFiles[:]

        for ignore in thingsToIgnore:
            logger.debug('ignoring ' + os.path.join(root, ignore))
            files[:] = [f for f in files if not fnmatch(f, ignore)]
            dirs[:] = [d for d in dirs if not fnmatch(d, ignore)]
            
    def preBackupHook(self, root, dirs, files):
        '''A method that is run before any directory in the backup
        hierarchy is processed. Most often will be used to remove
        files and subdirectories from the tree before the
        DirectoryBackupper class archives them. For example, all .o
        files could be removed.
        The default implementation does nothing.
        The arguments are the same as the values of the tuples
        produced by os.walk - the "root", or current directory being
        examined, "dirs" - a list of all subdirectory names of the
        current directory, and "files" - a list of all filenames in
        the current directory'''
        pass

    def preWalkHook(self, backupDir):
        pass
    
    def backup(self, backupDir):
        originalDir = os.path.abspath(os.curdir)
        os.chdir(os.path.abspath(self.workingDirectory))
        try:
            self.preWalkHook(backupDir)
            
            for root, dirs, files in os.walk(backupDir):
                self.preBackupHook(root, dirs, files)
                for f in files:
                    fullfile = os.path.join(root, f)
                    logger.debug('Adding ' + fullfile)
                    self.zipfile.write(fullfile)
        finally:
            os.chdir(originalDir)

    def close(self):
        self.zipfile.close()

class DocumentsBackupper(DirectoryBackupper):
    def __init__(self, outputFileName):
        DirectoryBackupper.__init__(self, outputFileName)

    def preBackupHook(self, root, dirs, files):
    	self.ignoreFileList( root, dirs, files, '.backupIgnore')
       
class SvnDirectoryBackupper(DirectoryBackupper):
    def __init__(self, outputFileName):
        DirectoryBackupper.__init__(self, outputFileName)
        
    def preBackupHook(self, root, dirs, files):
        """Removes SVN directories from the backup tree, as well as
        all files and directories that appear in the current
        directory's .svnignore file, if any."""
        if '.svn' in dirs:
            logger.debug('ignoring ' + os.path.join(root, '.svn'))
            dirs.remove('.svn')

        ignoreFiles = run('svn propget svn:ignore', root)
        self.ignoreFileList(root, dirs, files, [f for f in map(str.strip, ignoreFiles) if f])

class CvsDirectoryBackupper(DirectoryBackupper):
    def __init__(self, outputFileName):
        DirectoryBackupper.__init__(self, outputFileName)
        
    def preBackupHook(self, root, dirs, files):
        # TODO: extend to read ignores from ~/.cvsignore
        """Removes CVS directories from the backup tree, as well as
        all files and directories that appear in the current
        directory's .cvsignore file, if any."""
        if 'CVS' in dirs:
            logger.debug('ignoring ' + os.path.join(root, 'CVS'))
            dirs.remove('CVS')

        self.ignoreFileList(root, dirs, files, '.cvsignore')

def run(command, directory='.'):
    oldDir = os.path.abspath(os.curdir)
    os.chdir(os.path.abspath(directory))
    try:
        logger.debug('about to run "' + command + '" from "' + os.path.abspath(os.curdir) + '"')
        lines = os.popen(command).readlines()
        logger.debug('ran, and got this: ' + pprint.pformat(lines))
        return lines
    finally:
        os.chdir(oldDir)

class SparseSvnDirectoryBackupper:
    def __init__(self, outputFileName):
        self.outputFileName = os.path.abspath(outputFileName)
        self.workingDirectory = os.curdir

        self.zipfile = zipfile.ZipFile(self.outputFileName,
                                       mode='w',
                                       compression=zipfile.ZIP_DEFLATED)

    def backup(self, backupDir):
        originalDir = os.path.abspath(os.curdir)
        os.chdir(os.path.abspath(self.workingDirectory))
        try:
            lines = run('svn status --non-interactive', directory=backupDir)
            lines = [line[7:].strip() for line in lines if not line.startswith('Performing status on external item') and line[0] not in ' IDX! -']
            for f in lines:
                if f:
                    fullfile = os.path.join(backupDir, f)
                    logger.debug('Adding ' + fullfile)
                    if os.path.isdir(fullfile):
                        self.backupDirectory(fullfile)
                    else:
                        self.zipfile.write(fullfile)
        finally:
            os.chdir(originalDir)

    def preWalkHook(self, backupDir):
        logger.debug('preWalkHook')

        lines = [line[2:].strip() for line in run('svn status --non-interactive --quiet', directory=backupDir) if not line.startswith('Performing status on external item') and line[0] not in ' IDX']
        logger.debug('changed SVN files: ' + pprint.pformat(lines))
        self.lines = lines

    def preBackupHook(self, root, dirs, files):
        #SvnDirectoryBackupper.preBackupHook(self, root, dirs, files)
        slashyRoot = '/'.join(root.replace('\\', '/').split('/')[1:])
        logger.debug(str(files) + ' ' +  slashyRoot)
        files[:] = [file for file in files if slashyRoot + '/' + file in self.lines]
        
    def close(self):
        self.zipfile.close()

class SparseCvsDirectoryBackupper(CvsDirectoryBackupper):
    def __init__(self, outputFileName):
        CvsDirectoryBackupper.__init__(self, outputFileName)
        
    def preWalkHook(self, backupDir):
        logger.debug('preWalkHook')

        lines = [line[2:].strip() for line in run('cvs -f -q -n update', directory=backupDir) if line[0] in 'AMC?']
        logger.debug('changed CVS files: ' + pprint.pformat(lines))
        self.lines = lines

    def preBackupHook(self, root, dirs, files):
        CvsDirectoryBackupper.preBackupHook(self, root, dirs, files)
        slashyRoot = '/'.join(root.replace('\\', '/').split('/')[1:])
        files[:] = [file for file in files if slashyRoot + '/' + file in self.lines]
        

def main(args=None):
    if args == None:
        args = sys.argv
        d = CvsDirectoryBackupper(args[1] + '.zip')
        d.backup(args[1])
        d.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())

