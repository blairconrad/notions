#!/usr/bin/env python

import logging
import logging.config
logging.config.fileConfig('cruiseTrayIcon.config')


logger = logging.getLogger('cruiseTrayIcon')


from urllib import urlopen
from getopt import getopt, GetoptError
import wx
import time
import webbrowser
import sys
import subprocess
import ConfigParser

import growl

growler = growl.Growl('CruiseTray')
growler.register((
    growl.NotificationType('Build Failed'),
    growl.NotificationType('Build Fixed'),
    growl.NotificationType('Build')
    ))

CONFIG_FILE='cruiseTrayIcon.config'


def readConfig():
    result = []
    config = ConfigParser.ConfigParser()

    config.read(CONFIG_FILE)
    
    for section in config.sections():
        configurationOptions = ConfigurationOptions()
    
        configurationOptions.buildName = section
        if config.has_option(section, 'url'):
            configurationOptions.cruiseUrl = config.get(section, 'url')
        else:
            continue

        if config.has_option(section, 'goodIcon'):
            configurationOptions.goodIcon = config.get(section, 'goodIcon')

        if config.has_option(section, 'badIcon'):
            configurationOptions.brokenIcon = config.get(section, 'badIcon')

        if config.has_option(section, 'longTime'):
            configurationOptions.aLongTime = int(config.get(section, 'longTime'))

        result.append(configurationOptions)

    result.sort(key=lambda x: x.buildName)
    return result

oneSecond = 1000


BUILD_OK = 'OK'
BUILD_BROKEN = 'BROKEN'
RUNNING_A_LONG_TIME = 'RUNNING_A_LONG_TIME'
NO_CONTACT = 'NO_CONTACT'
UNKNOWN = 'UNKNOWN'

class ConfigurationOptions:
    def __init__(self):
        self.shouldShowStatusChangeDialog = True
        self.pollingDelay = oneSecond * 60
        self.cruiseUrl = "http://localhost:8080/scratch/cruise"
        self.buildFailedString = "BUILD FAILED"
        self.buildName = "The" # it works with the messages
        self.goodIcon = "green.ico"
        self.brokenIcon = "red.ico"
        self.badPageIcon = 'nocontact.ico'
        self.runningALongTimeIcon = 'clock.ico'
        self.aLongTime = 0 # seconds
        self.goodPageTitle = 'CruiseControl Build Results'

    def __str__(self):
        return str(self.__dict__)
    
class CruiseWatchingTrayIcon(wx.TaskBarIcon):
    def __init__(self, configOptions):
        wx.TaskBarIcon.__init__(self)
        self.buildStatus = UNKNOWN

        self.configurationOptions = configOptions

        wx.EVT_TASKBAR_LEFT_DCLICK(self, self.OnTaskBarLeftDClick)

    def OnTaskBarLeftDClick(self, evt):
        #print dir(evt.GetEventObject())
        #print evt.GetEventObject()
        webbrowser.open(self.configurationOptions.cruiseUrl)

    def buildEvent(self, message):
        growler.notify('Build', self.configurationOptions.buildName, text=message, url=self.configurationOptions.cruiseUrl)
        
    def buildFixed(self):
        growler.notify('Build', self.configurationOptions.buildName + ' fixed', url=self.configurationOptions.cruiseUrl)

    def buildBroken(self):
        logger.debug('build broken - config = ' + str(self.configurationOptions))
        growler.notify('Build', self.configurationOptions.buildName + ' broken', sticky=True, url=self.configurationOptions.cruiseUrl)

    def CheckBuild(self, evt):
        logger.debug('checking build - config = ' + str(self.configurationOptions))

        previousStatus = self.buildStatus
        self.buildStatus = self.getBuildStatus()

        if self.buildStatus == BUILD_BROKEN:
            icon = wx.Icon(self.configurationOptions.brokenIcon, wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon, self.configurationOptions.buildName + ' build is broken\n' +  self.buildingMessage)
        elif self.buildStatus == NO_CONTACT:
            icon = wx.Icon(self.configurationOptions.badPageIcon, wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon, self.configurationOptions.buildName + ' build status is unavailable')
            previousStatus = UNKNOWN
        elif self.buildStatus == RUNNING_A_LONG_TIME:
            icon = wx.Icon(self.configurationOptions.runningALongTimeIcon, wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon, self.configurationOptions.buildName + ' ' + self.buildingMessage)
            previousStatus = UNKNOWN
        else:
            icon = wx.Icon(self.configurationOptions.goodIcon, wx.BITMAP_TYPE_ICO)
            self.SetIcon(icon, self.configurationOptions.buildName + ' build is OK\n' + self.buildingMessage)

        if previousStatus == UNKNOWN:
            return
        if previousStatus == self.buildStatus:
            return
        if previousStatus == BUILD_BROKEN and self.buildStatus != BUILD_BROKEN:
            self.buildFixed()
        elif previousStatus != BUILD_BROKEN and self.buildStatus == BUILD_BROKEN:
            self.buildBroken()
        else:
            self.buildEvent('build status changed from ' + previousStatus + ' to '+ buildStatus)

    def isRunningALongTime(self, pageData):
        progressIndicator = 'progress: '
        indicatorStartPos = pageData.find(progressIndicator)
        if -1 != indicatorStartPos:
            startTimePos = indicatorStartPos + len(progressIndicator)
            endOfLinePos = pageData.find('\n', startTimePos)
            self.buildingMessage = pageData[startTimePos:endOfLinePos]
        else:
            self.buildingMessage = "doesn't appear to be building"

        # For now, always return false. We'll rehook up better detection later.
        return False

    def getBuildStatus(self):
        try:
            cruisePage = urlopen(self.configurationOptions.cruiseUrl, proxies={}).read()

            if self.isRunningALongTime(cruisePage):
                return RUNNING_A_LONG_TIME
            
            if not cruisePage.count(self.configurationOptions.goodPageTitle):
                # page is bad
                logger.debug('page: ' + cruisePage)
                logger.error('bad page - can\'t find ' + self.configurationOptions.goodPageTitle)
                return NO_CONTACT
            elif cruisePage.count(self.configurationOptions.buildFailedString):
                return BUILD_BROKEN
            else:
                return BUILD_OK
        except IOError, e:
            logger.exception('encountered an error when trying to contact self.configurationOptions.cruiseUrl')
            return NO_CONTACT


class CruiseWatchingTrayIconFrame(wx.Frame):
    def __init__(self, configurationOptionsList):
        wx.Frame.__init__(self, None, -1, '', size = (1, 1),
            style=wx.FRAME_NO_TASKBAR|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.configurationOptions = configurationOptionsList[0]
        if self.configurationOptions.shouldShowStatusChangeDialog:
            self.dlg = None
        else:
            self.dlg = "don't show the status change dialog please"
        self.lastBuildChecked = "something"
        
        self.children = []
        for configOption in configurationOptionsList:
            child = CruiseWatchingTrayIcon(configOption)
            self.children.append(child)
            wx.EVT_TASKBAR_RIGHT_DCLICK(child, self.OnTaskBarRightDClick)

        self.CheckBuild("whatever")
        self.SetIconTimer()
        self.Show(True)

    def OnTaskBarRightDClick(self, evt):
        #for child in self.children:
        #    child.tbicon.Close(True)
        #self.children = []

        #self.child.Destroy()
        #del(self.child)
        #self.child = None
        self.icontimer.Stop()
        for child in self.children:
            child.Destroy()
        self.Close(True)


        wx.GetApp().ProcessIdle()

    def SetIconTimer(self):
        wxId = wx.NewId()
        self.icontimer = wx.Timer(self, wxId)
        wx.EVT_TIMER(self, wxId, self.CheckBuild)
        self.icontimer.Start(self.configurationOptions.pollingDelay)

    def CheckBuild(self, evt):
        for child in self.children:
            child.CheckBuild(evt)

class CruiseWatchingTrayIconApp(wx.App):
    def __init__(self, someNumber, configurationOptionsList):
        self.configurationOptionsList = configurationOptionsList
        wx.App.__init__(self, someNumber)

    def OnInit(self):
        frame = CruiseWatchingTrayIconFrame(self.configurationOptionsList)
        frame.Center(wx.BOTH)
        frame.Show(False)
        return True

# def usage():
#     import os
#     print """Usage: """ + os.path.basename(sys.argv[0]).split('.')[0] + """ [options]
#        available options are:
#         -u urlOfCruiseWebPage (including http://)
#         -q (quiet = no dialog box on status change)
#         -d pollingDelayInSeconds (how long it waits between polling cruise)
#         -b buildFailedString (existence on cruise page means build broken)
#         -n human-readable name for this build (used on icon mouseover)
#         -g green icon file, for good build - default is green.ico
#         -r red icon file, for bad builds - default is red.ico
#         -t the number of seconds after which the build is considered late - default is 3600
#         -h (help - show this message)"""

def main():
    growler.notify('Build', 'CruiseTrayIcon starting', url='http://google.ca/')
    CruiseWatchingTrayIconApp(0, readConfig()).MainLoop()

if __name__ == '__main__':
    main()
#     try:
#         opts, noArgsExpected = getopt(sys.argv[1:], "qhd:u:n:b:r:g:t:", [])
#     except GetoptError:
#         usage()
#         sys.exit(2)
#     configurationOptions = ConfigurationOptions()
#     for o, a in opts:
#         if o == "-q":
#             configurationOptions.shouldShowStatusChangeDialog = False
#         if o == "-d":
#             configurationOptions.pollingDelay = int(a) * oneSecond
#         if o == "-u":
#             configurationOptions.cruiseUrl = a
#         if o == "-b":
#             configurationOptions.buildFailedString = a
#         if o == "-n":
#             configurationOptions.buildName = a
#         if o == "-r":
#             configurationOptions.brokenIcon = a
#         if o == "-g":
#             configurationOptions.goodIcon = a
#         if o == "-t":
#             configurationOptions.aLongTime = int(a)
#         if o == "-h":
#             usage()
#             sys.exit()
