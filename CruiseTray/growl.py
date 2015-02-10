#!/usr/bin/env python

import sys
import socket

class NotificationType:
    def __init__(self, name, display_name=None, enabled=True, icon=None):
        self.name = name
        self.display_name = display_name or name
        self.enabled = enabled
        self.icon = icon

class Growl:
    def __init__(self, application_name='Python/Growl', host='localhost', port=23053):
        self.application_name = application_name
        self.host = host
        self.port = port
        self.debug = True
        self.registered = False
        self.registration_failed = False
    
    def send(self, lines):
        print 'not registered, so not sending:', lines
        
    def _send(self, lines):
        message = '\r\n'.join((line.replace('\n', '\\n') for line in lines)) + '\r\n\r\n'
        if self.debug:
            print 'Message:\n ', message.replace('\r\n', '\r\n  ')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.debug:
            print 'connecting'
        s.connect((self.host, self.port))

        if self.debug:
            print 'sending'
        s.send(message)
        if self.debug:
            print 'receiving'
        result = ''
        new_data = s.recv(1024)

        while len(new_data) == 1024 :
            result += new_data
            new_data = s.recv(1024)
        result += new_data
        s.close()

        if self.debug:
            print 'Received:\n ', result.replace('\r\n', '\r\n  ')

    def register(self, notification_types=None):
        if self.registered:
            return
        if notification_types:
            self.notification_types = notification_types
        if not self.notification_types:
            return
        lines = ['GNTP/1.0 REGISTER NONE',
                 'Application-Name: ' + self.application_name,
                 'Notifications-Count: ' + str(len(self.notification_types)),
                 ]
        for notification_type in self.notification_types:
            lines.extend(['',
                          'Notification-Name: ' + notification_type.name,
                          #'Notification-Icon: http://myorganized.info/images/solution.png?1241093522',
                          ])
            if not notification_type.enabled:
                lines.append('Notification-Enabled: false')

        try:
            self._send(lines)
            self.send = self._send
            self.registered = True
        except Exception as e:
            if not self.registration_failed:
                print 'Could not register - turning off growling. Error:\n', e
            self.registration_failed = True
            

    def notify(self, name, title, text=None, sticky=False, url=None):
        self.register()
        lines = ['GNTP/1.0 NOTIFY NONE',
                 'Application-Name: ' + self.application_name,
                 'Notification-Name: ' + name,
                 'Notification-Title: ' + title,
                 ]
        if text:
            lines.append('Notification-Text: ' + title)
            
        if sticky:
            lines.append('Notification-Sticky: true')

        if url:
            lines.append('Notification-Callback-Target: ' + url)

        self.send(lines)

def main(args=None):
    if args == None:
        args = sys.argv[1:]
    return 0


if __name__ == '__main__':
    growl = Growl('My App')
    growl.register(
        (
        NotificationType('notification type 1'),
        ))
    #growl.notify('notification type 1', 'title', 'notification text sticky=true', sticky=True)
    growl.notify('notification type 1', 'title', 'notification text sticky=true', sticky=True, url='http://libraryhippo.appspot.com/')
#    growl.notify('notification type 1', 'title', 'notification text sticky=false', sticky=False)
#    growl.notify('notification type 1', 'title', 'notification text no sticky')
