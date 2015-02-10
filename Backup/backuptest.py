#!/usr/env/bin python

import unittest
import backup
import zipfile

import os

def makeTree(fileSystem, baseDir=None):
    for name, value in fileSystem.items():
        if baseDir:
            name = os.path.join(baseDir, name)

        if type('') == type(value):
            f = file(name, 'w')
            f.write(value)
            f.close()
        elif type({}) == type(value):
            os.mkdir(name)
            makeTree(value, name)

def removeTree(fileSystem, baseDir=None):
    for name, value in fileSystem.items():
        if baseDir:
            name = os.path.join(baseDir, name)
            
        if type('') == type(value):
            os.unlink(name)
        elif type({}) == type(value):
            removeTree(value, name)
            os.rmdir(name)
            
class BackupperTester(unittest.TestCase):
    def removeTree(self, dirName):
        for root, dirs, files in os.walk(dirName, topdown=False):
            #print root, dirs, files
            for file in files:
                #print 'Unlinking', root + '/' + file
                os.unlink(os.path.join(root, file))
            for dir in dirs:
                #print 'DirRemoving', root + '/' + dir + '/'
                os.removedirs(os.path.join(root, dir))

        if os.path.isdir(dirName):
            #print 'Unrooting', dirName + '/'
            os.removedirs(dirName)
            
    def testBackupOneFileDir(self):
        testDirName = 'onefiledir'
        
        tree = {testDirName:
                {'onefile': 'abc' * 10000}
                }
        makeTree(tree)

        b = backup.DirectoryBackupper(testDirName + '.zip')
        b.backup(testDirName)
        b.close()

        self.removeTree('onefiledir')
        
        z = zipfile.ZipFile(testDirName + '.zip')
        contents = z.infolist()
        z.close()

        self.assertEqual(1, len(contents))
        self.assertEqual(testDirName + '/onefile', contents[0].filename)
        self.assertEqual(30000, contents[0].file_size)

        os.unlink(testDirName + '.zip')
        
    def testWorkingDirectoryWorks(self):
        testDirName = 'thedir'
        
        tree = {testDirName:
                {'anotherdir':
                 {'onefile': 'abc' * 10000}
                 }
                }
        makeTree(tree)

        b = backup.DirectoryBackupper('anotherdir.zip')
        b.workingDirectory = testDirName
        b.backup('anotherdir')
        b.close()

        self.removeTree(testDirName)
        
        z = zipfile.ZipFile('anotherdir.zip')
        contents = z.infolist()
        z.close()

        self.assertEqual(1, len(contents))
        self.assertEqual('anotherdir/onefile', contents[0].filename)
        self.assertEqual(30000, contents[0].file_size)

        os.unlink('anotherdir.zip')
        
class CvsBackupperTester(BackupperTester):
    def testBackupIgnoresCvs(self):
        testDirName = 'dirwithcvs'
        
        if os.path.isfile(testDirName + '.zip'):
            os.unlink(testDirName + '.zip')

        self.removeTree(testDirName)
        os.mkdir(testDirName)

        f = file(os.path.join(testDirName, 'onefile'), 'w')
        f.write('abc' * 10000)
        f.close()

        os.mkdir(os.path.join(testDirName, 'CVS'))
        f = file(os.path.join(testDirName, 'CVS', 'cvsfile'), 'w')
        f.write('abc' * 10000)
        f.close()
        
        b = backup.CvsDirectoryBackupper(testDirName + '.zip')
        b.backup(testDirName)
        b.close()

        z = zipfile.ZipFile(testDirName + '.zip')
        contents = z.infolist()
        z.close()

        self.assertEqual(1, len(contents))
        self.assertEqual(testDirName + '/onefile', contents[0].filename)
        self.assertEqual(30000, contents[0].file_size)

        self.removeTree(testDirName)
        os.unlink(testDirName + '.zip')

    def testBackupIgnoresCvsignore(self):
        testDirName = 'dirwithcvsignore'
        
        if os.path.isfile(testDirName + '.zip'):
            os.unlink(testDirName + '.zip')

        self.removeTree(testDirName)
        os.mkdir(testDirName)

        f = file(os.path.join(testDirName, 'onefile'), 'w')
        f.write('abc' * 10000)
        f.close()

        f = file(os.path.join(testDirName, 'twofile'), 'w')
        f.write('def' * 10000)
        f.close()

        f = file(os.path.join(testDirName, '.cvsignore'), 'w')
        f.write('twofile\n')
        f.close()

        b = backup.CvsDirectoryBackupper(testDirName + '.zip')
        b.backup(testDirName)
        b.close()

        z = zipfile.ZipFile(testDirName + '.zip')
        contents = z.infolist()
        z.close()

        self.assertEqual(2, len(contents))
        self.assertEqual(testDirName + '/onefile', contents[0].filename)
        self.assertEqual(30000, contents[0].file_size)

        self.removeTree(testDirName)
        os.unlink(testDirName + '.zip')

    def testBackupIgnoresCvsignoreGlobFiles(self):
        testDirName = 'dirwithcvsignore'
        
        tree = {testDirName:
                {'onefile': 'abc' * 10000,
                 'twofile': 'def' * 10000,
                 '.cvsignore': 'two*ile\n',
                 }
                }
                 
        if os.path.isfile(testDirName + '.zip'):
            os.unlink(testDirName + '.zip')

        self.removeTree(testDirName)

        makeTree(tree)

        b = backup.CvsDirectoryBackupper(testDirName + '.zip')
        b.backup(testDirName)
        b.close()

        self.removeTree(testDirName)

        z = zipfile.ZipFile(testDirName + '.zip')
        contents = z.infolist()
        z.close()

        self.assertEqual(2, len(contents))
        self.assertEqual(testDirName + '/onefile', contents[0].filename)
        self.assertEqual(30000, contents[0].file_size)

        os.unlink(testDirName + '.zip')

    def testBackupIgnoresCvsignoreGlobFiles(self):
        testDirName = 'dirwithcvsignore'

        tree = {testDirName:
                {'onefile': 'abc' * 10000,
                 '.cvsignore': 'tw*ir\n',
                 'twodir':
                 {'twofile': 'def' * 10000}
                 }
                }
                 
        if os.path.isfile(testDirName + '.zip'):
            os.unlink(testDirName + '.zip')

        self.removeTree(testDirName)

        makeTree(tree)
        
        b = backup.CvsDirectoryBackupper(testDirName + '.zip')
        b.backup(testDirName)
        b.close()

        self.removeTree(testDirName)
        
        z = zipfile.ZipFile(testDirName + '.zip')
        contents = z.infolist()
        z.close()

        self.assertEqual(2, len(contents))
        #self.assertEqual(testDirName + '/onefile', contents[0].filename)
        #self.assertEqual(30000, contents[0].file_size)

        self.removeTree(testDirName)
        os.unlink(testDirName + '.zip')
