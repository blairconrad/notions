#!/usr/bin/env python

import sys
import string
import os
import colorsys

import BaseHTTPServer
import threading


def loadInDefaultBrowser(html):
    """Display html in the default web browser without creating a temp file.

    Instantiates a trivial http server in a background thread and calls
    os.startfile with a URL to retrieve html from that server.
    """

    class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_GET(self):
            bufferSize = 8 * 1024
            for i in xrange(0, len(html), bufferSize):
                self.wfile.write(html[i : i + bufferSize])

    server = BaseHTTPServer.HTTPServer(("localhost", 0), RequestHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()
    os.startfile("http://localhost:" + str(server.server_port))
    thread.join()


def cmpVersion(v1, v2):
    def cmp(t1, t2):
        if t1 is None:
            return -1
        elif t2 is None:
            return 1
        else:
            return t1 - t2

    sv1 = map(int, string.split(v1, "."))
    sv2 = map(int, string.split(v2, "."))
    results = map(cmp, sv1, sv2)
    for res in results:
        if res != 0:
            return res
    return 0


class Source:
    def __init__(self, input):
        (self.version, rest) = string.split(input, "(", 1)
        self.version = string.strip(self.version)
        rest = string.split(rest, ")")[0]
        (self.author, self.date) = string.split(rest)

    def __str__(self):
        return self.version + " " + self.author + " " + self.date

    def get_author(self):
        return self.author

    def get_version(self):
        return self.version

    def get_date(self):
        return self.date

    def same_author(self, other):
        return self.author == other.author

    def same_date(self, other):
        return self.date == other.date

    def same_version(self, other):
        return self.version == other.version


class ColourMapper:
    def __init__(self):
        self.sources = {}

    def add(self, one_source):
        self.sources[one_source.get_version()] = one_source

    def get_version_colour(self, version):
        return self.colours_by_version[version]

    def generate_colours(self):
        def remove_duplicates(a_list):
            a_list.sort()
            i = 1
            while i < len(a_list):
                if a_list[i] == a_list[i - 1]:
                    del a_list[i]
                else:
                    i = i + 1
            return None

        authors = map(Source.get_author, self.sources.values())
        remove_duplicates(authors)

        versions_by_author = {}
        map(
            lambda a: versions_by_author.setdefault(
                a, map(Source.get_version, filter(lambda x: x.get_author() == a, self.sources.values()))
            ),
            authors,
        )

        # does this really sort?
        map(lambda l: l.sort(cmpVersion), versions_by_author.values())

        # sys.stderr.write(str(authors) + '\n')
        # sys.stderr.write(str(versions_by_author) + '\n')

        self.colours_by_version = {}
        for (author, versions) in versions_by_author.items():
            for index in range(len(versions)):
                this_val = 1.0 - 0.5 * (index + 1) / (len(versions) + 1)
                this_hue = 1.0 * authors.index(author) / len(authors)
                this_sat = 0.5
                (r, g, b) = colorsys.hsv_to_rgb(this_hue, this_sat, this_val)
                # print this_val, this_hue, this_sat, r, g, b, author, versions[index]
                self.colours_by_version[versions[index]] = "%02X%02X%02X" % (256 * r, 256 * g, 256 * b)
                # sys.stderr.write(author + ' ' +  versions[index] + ' ' + str(rgb) + '\n')


def escape_html_chars(input):
    output = string.replace(input, "&", "&amp;")
    output = string.replace(output, "<", "&lt;")
    output = string.replace(output, ">", "&gt;")
    output = string.replace(output, " ", "&nbsp;")
    output = string.replace(output, "\t", "&nbsp;" * 8)
    return output


def makeHtml(args):

    filename = " ".join(args)
    lines = os.popen("cvs annotate " + filename).readlines()

    result = (
        """<html>
    <head>
    <title>Annotated %(filename)s</title>
    <style type="text/css">
    body {
    background-color: #EEEEEE;
    }
       .revision {
                vertical-align: top;
                margin: 0;
                font-family: monospace;
                padding: 0;
             }

       .code {
                vertical-align: top;

                margin: 0;
                font-family: monospace;
                padding: 0;
            background-color: white;
             }
       tr {
                margin: 0;
                padding: 0;
          }


    </style>
    </head>
    <body>
    <h1>Annotated %(filename)s</h1>
    <table>
    """
        % vars()
    )

    stuff = []

    for line in lines:
        (head, rest) = string.split(line, ":", 1)
        rest = string.rstrip(rest)
        source = Source(head)
        body = escape_html_chars(rest)
        stuff.append((source, body))

    code_groups = []
    last_source = None
    lines = []

    cm = ColourMapper()
    for (source, body) in stuff:
        cm.add(source)

    cm.generate_colours()
    for (source, body) in stuff:
        if last_source is not None and source.get_version() == last_source.get_version():
            lines.append(body)
        else:
            if len(lines) > 0:
                code_groups.append((last_source, lines))
            lines = [body]
            last_source = source
    if len(lines) > 0:
        code_groups.append((last_source, lines))

    for group in code_groups:
        source = group[0]
        body = group[1]
        result += '<tr><td class="revision" style="background-color: #%s">%s</td><td class="code">%s</td></tr>' % (
            cm.get_version_colour(source.get_version()),
            source,
            string.join(body, "<br>\n"),
        )

    result += """</table>
    </body>
    </html>"""
    return result


def main(args=None):
    if args is None:
        args = sys.argv

    result = makeHtml(sys.argv[1:])
    loadInDefaultBrowser(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
