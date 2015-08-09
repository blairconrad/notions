#!/usr/bin/env python

import sys
import re
import urllib2
import os
import time
import optparse

# Here are the email pacakge modules we'll need
import email.MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart

import smtplib

verbose = False

def log(s):
    global verbose
    if verbose:
        print s

class MailSender:
    def __init__(self):
        self.mime_version = '1.0';
        self.setContentType('html')
    # end def __init__

    def setContentType(self, newContentType):
        self.contentType = newContentType
    # end def setContentType
    

    def send(self, fromAddress, toAddresses, subject, images):
        mailText = '''<html><body>\n'''
        for source, url in images:
            if url:
                mailText += '<img alt="' + source + '" src="' + url + '"><br>\n'
            else:
                mailText += "Couldn't find comic for " + source + "<br>\n"
        mailText += '</body></html>'

        if ( type(toAddresses) == type("") ):
            toAddresses = [toAddresses];
           
        msg = email.MIMEText.MIMEText(mailText, self.contentType)
        msg['Subject'] = subject
        msg['To'] = ', '.join(toAddresses)

        s = smtplib.SMTP()
        s.connect('mailhost')
        s.sendmail(fromAddress, toAddresses, msg.as_string())
        s.close()

    def sendPics(self, fromAddress, toAddresses, subject, images):
        if ( type(toAddresses) == type("") ):
            toAddresses = [toAddresses];
           
        msg = email.MIMEMultipart.MIMEMultipart()
        msg['Subject'] = subject
        msg['To'] = ', '.join(toAddresses)
        msg['From'] = fromAddress
        msg.preamble = 'Pics'
        msg.epilogue = ''
        
        for source, url in images: 
            data = urllib2.urlopen(url).read()
            img = MIMEImage(data)
            msg.attach(img)

        s = smtplib.SMTP()
        s.connect('mailhost')
        s.sendmail(fromAddress, toAddresses, msg.as_string())
        s.close()
        
        

    #end def send
# end class MailSender

def comicToSite(comic):
    if comic == 'dilbert':
        return 'www.dilbert.com'
    else:
        return 'www.gocomics.com'

def siteToRegexp(site):
    if site == 'www.dilbert.com':
        return re.compile('data-image="([^"]+)"')
    else:
        return re.compile('class="strip" src="([^"]+)" />')
    
def FindImage(sourceName, sourceText):
    try:
        matches = siteToRegexp(comicToSite(sourceName)).findall(sourceText)
        log(matches)
        if matches[0].startswith('http:'):
            return matches[0]
        else:
            return 'http://' + comicToSite(sourceName) + matches[0]
    except:
        return None

def FindImages(sources):
    matches = {}
    for (sourceName, sourceText) in sources.items():
        matches[sourceName] =  (sourceName, FindImage(sourceName, sourceText))
    return matches

class UrlMapper:
    def __init__(self):
        self.urls = {
            'dilbert': 'http://www.dilbert.com/',
            }

    def getUrl(self, comic):
        return self.urls.get(comic, 'http://' + comicToSite(comic) + '/' + comic)

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    def username():
        return os.environ.get('USER', os.environ.get('LOGNAME', os.environ['USERNAME']))

    global verbose
    
    parser = optparse.OptionParser()
    parser.add_option("--inline", action="store_true", dest="inlineImages", default=False,
                      help="inline images, rather than sending IMG SRCs")
    parser.add_option("--verbose", action="store_true", dest="verbose", default=False,
                      help="log verbosely")
    (options, args) = parser.parse_args(args)

    verbose = options.verbose

    mailTo = args[0]
    comics = args[1:]
    sources = {}

    um = UrlMapper()

    for comic in comics:
        log(um.getUrl(comic))
        sources[comic] = urllib2.urlopen(um.getUrl(comic)).read()
        log(sources[comic])
    images = FindImages(sources).values()

    m = MailSender()
    if options.inlineImages:
        m.sendPics(username() + '@mitra.com', [mailTo], 'comics ' + time.strftime('%d %B %Y'), images)
    else:
        m.send(username() + '@mitra.com', [mailTo], 'comics ' + time.strftime('%d %B %Y'), images)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

