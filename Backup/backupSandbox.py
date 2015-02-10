#!/usr/bin/env python

import logging
import logging.config

CONFIG_FILE='backupSandbox.config'
# Set up the logger
logging.config.fileConfig(CONFIG_FILE)
logger = logging.getLogger('backup.backupSandbox')

import sys
import time
import os.path
import ConfigParser
import glob
import removeDuplicateFiles
import backup

def getBackupper(name, outputFile):
    c = compile('backup.' + name +  '(outputFile)', '<string>', 'eval')
    return eval(c)

class TargetConfig:
    def __init__(self, name, sourceDir, outputDir, outputFile='%Y.%m.%d_%H.%M.%S.zip', backupper='DocumentsBackupper'):
        self.name = name
        self.sourceDir = sourceDir
        self.outputDir = outputDir
        self.outputFile = os.path.join(outputDir, outputFile)
        self.backupper = backupper

def loadTargetConfig(config, targetName):
    logger.info('loading configuration for ' + targetName)

    sourceDir = os.path.abspath(config.get(targetName, 'sourceDir'))
    outputDir, outputFile = os.path.split(os.path.abspath(config.get(targetName, 'outputFile')))
    return TargetConfig(targetName, sourceDir, outputDir, outputFile, config.get(targetName, 'backupper'))

def main(args=None):

    if args == None:
        args = sys.argv[1:]

    targets = []
    if len(args) > 0:
        sourceDir = os.path.abspath(args[0])
        outputDir = os.path.abspath(args[1])
        if len(args) > 2:
            backupper = args[2]
            targets.append(TargetConfig(sourceDir, outputDir, backupper=backupper))
        else:
            targets.append(TargetConfig(sourceDir, outputDir))
    else:
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_FILE)

        for section in config.sections():
            if config.has_option(section, 'sourceDir') and config.has_option(section, 'outputFile'):
                targets.append(loadTargetConfig(config,section))
            else:
                logger.debug('skipping ' + section)

    for target in targets:
        logger.info('starting backup ' + target.name)
        if not os.path.isdir(target.outputDir):
            os.makedirs(target.outputDir)

        b = getBackupper(target.backupper, time.strftime(target.outputFile))
        b.workingDirectory = os.path.split(target.sourceDir)[0]
        b.backup(os.path.split(target.sourceDir)[1])
        b.close()

        logger.debug('cleaning directory ' + target.outputDir)
        removeDuplicateFiles.cleanDir(target.outputDir)
        logger.info('finished with backup ' + target.name)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
