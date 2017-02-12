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

import smtplib


verbose = False


def log(s):
    global verbose
    if verbose:
        print s


class MailSender:
    def __init__(self):
        self.mime_version = '1.0'
        self.set_content_type('html')

    def set_content_type(self, new_content_type):
        self.content_type = new_content_type

    def send(self, from_address, to_addresses, subject, images):
        mail_text = '''<html><body>\n'''
        for source, url in images:
            if url:
                mail_text += '<img alt="' + source + '" src="' + url + '"><br>\n'
            else:
                mail_text += "Couldn't find comic for " + source + "<br>\n"
        mail_text += '</body></html>'

        msg = email.MIMEText.MIMEText(mail_text, self.content_type)
        msg['Subject'] = subject
        msg['To'] = ', '.join(to_addresses)

        s = smtplib.SMTP()
        s.connect('mailhost')
        s.sendmail(from_address, to_addresses, msg.as_string())
        s.close()

    def send_pics(self, from_address, to_addresses, subject, images):
        msg = email.MIMEMultipart.MIMEMultipart()
        msg['Subject'] = subject
        msg['To'] = ', '.join(to_addresses)
        msg['From'] = from_address
        msg.preamble = 'Pics'
        msg.epilogue = ''

        for source, url in images:
            data = load_url(url)
            img = MIMEImage(data)
            msg.attach(img)

        s = smtplib.SMTP()
        s.connect('mailhost')
        s.sendmail(from_address, to_addresses, msg.as_string())
        s.close()


def comic_to_site(comic):
    if comic == 'dilbert':
        return 'www.dilbert.com'
    if comic in ['blondie', 'rhymes-with-orange']:
        return 'comicskingdom.com'
    else:
        return 'www.gocomics.com'


def site_to_regexp(site):
    if site == 'www.dilbert.com':
        return re.compile('data-image="([^"]+)"')
    else:
        return re.compile('data-image="([^"]+)"')


def find_image(source_name, source_text):
    try:
        matches = site_to_regexp(comic_to_site(source_name)).findall(source_text)
        log(matches)
        if matches[0].startswith('http:'):
            return matches[0]
        else:
            return 'http://' + comic_to_site(source_name) + matches[0]
    except:
        return None


def find_images(sources):
    matches = {}
    for (source_name, source_text) in sources.items():
        matches[source_name] = (source_name, find_image(source_name, source_text))
    return matches


class UrlMapper:
    def __init__(self):
        self.urls = {
            'dilbert': 'http://www.dilbert.com/',
            }

    def get_url(self, comic):
        return self.urls.get(comic, 'http://' + comic_to_site(comic) + '/' + comic)


def load_url(url):
    log('opening ' + url)
    request = urllib2.Request(url)
    request.add_header(
        'User-Agent',
        ' '.join(['Mozilla/5.0 (Windows NT 6.1; WOW64)',
                  'AppleWebKit/537.36 (KHTML, like Gecko)',
                  'Chrome/40.0.2214.93',
                  'Safari/537.36']))
    return urllib2.urlopen(request).read()


def save_comic(path, comic, source):
    with open(path + '/' + comic + '.html', 'wb') as f:
        f.write(source)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    def username():
        return os.environ.get('USER', os.environ.get('LOGNAME', os.environ['USERNAME']))

    global verbose

    parser = optparse.OptionParser()
    parser.add_option("--inline", action="store_true", dest="inline_images", default=False,
                      help="inline images, rather than sending IMG SRCs")
    parser.add_option("--verbose", action="store_true", dest="verbose", default=False,
                      help="log verbosely")
    parser.add_option("--save", dest="save_path", default=None,
                      help="save comics' web pages to PATH", metavar="PATH")
    (options, args) = parser.parse_args(args)

    verbose = options.verbose

    mail_to = args[0]
    comics = args[1:]
    sources = {}

    um = UrlMapper()

    for comic in comics:
        url = um.get_url(comic)
        sources[comic] = load_url(url)
        if options.save_path:
            save_comic(options.save_path, comic, sources[comic])
        log(sources[comic])
    images = find_images(sources).values()

    m = MailSender()
    if options.inline_images:
        m.send_pics(username() + '@mitra.com', [mail_to], 'comics ' + time.strftime('%d %B %Y'), images)
    else:
        m.send(username() + '@mitra.com', [mail_to], 'comics ' + time.strftime('%d %B %Y'), images)

    return 0


if __name__ == '__main__':
    sys.exit(main())
