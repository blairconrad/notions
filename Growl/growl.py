#!/usr/bin/env python

import sys
import socket

class Growl:
    def __init__(self, application_name='Python/Growl', host='localhost', port=23053):
        self.application_name = application_name
        self.host = host
        self.port = port
    
    def send(self, message):
        print message
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'connecting'
        s.connect((self.host, self.port))
        print 'sending'
        s.send(message)
        print 'receiving'
        result = ''
        new_data = s.recv(1024)

        while len(new_data) == 1024 :
            result += new_data
            new_data = s.recv(1024)
        result += new_data
        s.close()
        print 'Received:\n', result

    def register(self, notification_types):
        message = 'GNTP/1.0 REGISTER NONE\r\nApplication-Name: %s\r\nNotifications-Count: %d\r\n\r\n' % (self.application_name, len(notification_types))
        for notification_type in notification_types:
            message += 'Notification-Name: %s\r\n\r\n' % notification_type
        self.send(message)

    def notify(self, name, title):
        message = '\r\n'.join(('GNTP/1.0 NOTIFY NONE',
                               'Application-Name: %s',
                               'Notification-Name: %s',
                               'Notification-Title: %s')) % (self.application_name, name, title)
        message += '\r\n\r\n'
        self.send(message)

def main(args=None):
    if args == None:
        args = sys.argv[1:]
    return 0


if __name__ == '__main__':
    growl = Growl('My App')
    growl.register(('notification type 1', 'notification type 2'))
    growl.notify('notification type 1', 'title')
