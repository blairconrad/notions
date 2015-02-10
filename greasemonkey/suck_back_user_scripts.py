#!/usr/bin/env python

import sys
import shutil
import os
import glob

"""An array of (<source file name>, <installed file name>) pairs"""
filesToCopy = [
    ('XisbnLibraryLookupWpl.user.js', 'xisbnlibrarylookupwaterl.user.js'),
    ('fixWplPort.user.js', 'fixwplport.user.js'),
    ('LinkifyLibraryElf.user.js', 'LinkifyLibraryElf.user.js'),
    ('wpl_ui_improvements.user.js', 'wpl_ui_improvements/wpl_ui_improvements.user.js'),
    ('amazoncalocalizer.user.js', 'amazoncalocalizer.user.js'),
    ('pbembackgammonfixer.user.js', 'pbembackgammonfixer.user.js'),
    ('PrettifyMis.user.js', 'prettifymis/prettifymis.user.js'),
    ('cruisecontrolbuildresult.user.js', 'cruisecontrol_build_resu/cruisecontrol_build_resu.user.js'),
    ('environmentcanadabetterw.user.js', 'environmentcanadabetterw.user.js'),
    ('automatic_livelink_login.user.js','automatic_livelink_login/automatic_livelink_login.user.js'),
    ('stack_overflow_restrict.user.js', 'stack_overflow_restrict_/stack_overflow_restrict_.user.js'),
    ('stack_overflow_add_post_references.user.js', 'stack_overflow_add_post_/stack_overflow_add_post_.user.js'),
    ('confluence_minor_change_.user.js', 'confluence_minor_change_/confluence_minor_change_.user.js'),
    ('remove_useless_mis_revis.user.js', 'remove_useless_mis_revis/remove_useless_mis_revis.user.js'),
    ]


THISDIR = 0
GMDIR = 1

def getGmPath():
    path = r'\%s\PortableApps\FirefoxPortable\Data\profile' % os.environ['USERNAME']

    if not os.path.exists(path):
        appDataPath = os.environ['APPDATA']
        profilePaths = glob.glob(os.path.join(appDataPath, 'Mozilla', 'Firefox', 'Profiles', '*.default'))
        if len(profilePaths) == 0:
            raise "couldn't fine profile path"
        elif len(profilePaths) > 1:
            raise 'more than one Firefox profile path'
        else:
            path = profilePaths[0]
    return os.path.join(path, 'gm_scripts')

def copyFile(sourceFile, destFile):
    if not os.path.exists(destFile):
        print os.path.split(destFile)[1], 'doesn\'t exist - not copying'
        return

    if not os.path.exists(sourceFile):
        print os.path.split(sourceFile)[1], 'doesn\'t exist - not copying'
        return

    #print os.stat(destFile).st_mtime, os.stat(sourceFile).st_mtime
    if os.stat(destFile).st_mtime > os.stat(sourceFile).st_mtime:
        print os.path.split(destFile)[1], 'is as new as', os.path.split(sourceFile)[1], '- skipping'
    else:
        print os.path.split(sourceFile)[1], ': copying to', os.path.split(destFile)[1]
        shutil.copy(sourceFile, destFile)
        shutil.copystat(sourceFile, destFile)

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    gmPath = getGmPath();

    for fileToCopy in filesToCopy:
        sourceFile = os.path.join(gmPath, fileToCopy[GMDIR])
        destFile = fileToCopy[THISDIR]
        copyFile(sourceFile, destFile)
    return 0


if __name__ == '__main__':
    sys.exit(main())

