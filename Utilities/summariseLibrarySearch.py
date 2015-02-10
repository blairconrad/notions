#!/usr/bin/env python

import sys
import urllib2
import HTMLParser
import pprint

class ItemPageParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.items = []
        self.inTr = False
        self.inItemNumber = False
        self.inItemLink = False
        self.inItemYear = False
        self.nextItem = None
        self.justGotLink = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.inTr = True
        elif tag == 'td' and self.inTr:
            if len(attrs) == 2 and attrs[1][0] == 'class' and attrs[1][1] == 'browseEntryNum':
                self.inItemNumber = True
            if len(attrs) == 4 and attrs[3][0] == 'class' and attrs[3][1] == 'browseEntryYear':
                self.inItemYear = True
        elif tag == 'a' and self.inTr:
            self.inItemLink = True
            self.justGotLink = False
            self.nextItem = {'link': attrs[0][1]}
            

    def handle_data(self, data):
        if self.inItemYear:
            self.nextItem['year'] = data.strip()
        elif self.inItemLink:
            self.nextItem['title'] = data.strip()
        elif self.inTr and self.justGotLink:
            self.justGotLink = False
            self.nextItem['details'] = data.strip()

    def handle_endtag(self, tag):
        if tag == 'td':
            if self.inItemNumber:
                self.inItemNumber = False
            elif self.inItemYear:
                self.inItemYear = False
                if self.nextItem:
                    self.items.append(self.nextItem)
                    self.nextItem = None
        elif tag == 'a':
            if self.inItemLink:
                self.inItemLink = False
                self.justGotLink = True
        elif tag == 'tr':
            self.inTr = False

def sortItems(items, tag):
    markedItems = [(x[tag], x['title'], x) for x in items]
    markedItems.sort()
    return [x[2] for x in markedItems]

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    increment = 12
    baseUrl = 'http://books.wpl.ca/search/dFeature+films/dfeature+films/1,4,1321,B/exact&FF=dfeature+films&1,1302'
    #baseUrl = 'http://books.wpl.ca/search/dFeature+films+china/dfeature+films+china/1,1,17,B/exact&FF=dfeature+films+china&1,17'

    records = baseUrl.split('&')[-1]
    urlBeforeRecords = baseUrl[0:-len(records)]
    #print urlBeforeRecords

    lastRecord = int(records.split(',')[-1])
    #print lastRecord

    firstRecordOnThisPage = int(records.split(',')[0])
    #print firstRecordOnThisPage

    allItems = []
    output = file('output.html', 'wb')

    output.write('''<html><body><table border="1">\n''')
    while firstRecordOnThisPage < lastRecord:
        nextUrl = urlBeforeRecords + str(firstRecordOnThisPage) + ',' + str(lastRecord)
        #print firstRecordOnThisPage
        #print nextUrl
        u = ItemPageParser()
        u.feed(urllib2.urlopen(nextUrl).read())

        #pprint.pprint(u.items)
        allItems.extend(u.items)
        firstRecordOnThisPage += increment

    allItems = [x for x in allItems if -1 != x['details'].find('[DVD]')]

    for item in allItems:
        newYear = ''
        for char in item['year']:
            if char.isdigit():
                newYear += char
        item['year'] = newYear
    allItems = sortItems(allItems, 'year')
    for item in allItems:
        #print item
        output.write('<tr><td><a href="http://books.wpl.ca%(link)s">%(title)s</a></td><td>%(year)s</td></tr>\n' % item)
    output.write('</table></body></html>')
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

