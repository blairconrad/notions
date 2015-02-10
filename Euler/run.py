#!/usr/bin/env python

import datetime
import glob
import imp
import os
import sys
import optparse

def do_main(args):
    sys.path.append('..')

    parser = optparse.OptionParser()
    parser.add_option("--show-skip",
                      action="store_true", dest="show_skip", default=False,
                      help="show skipped tests")

    (options, args) = parser.parse_args()

    if len(args) == 0:
        questions = glob.glob('q*')
        questions.sort()
    else:
        questions = glob.glob(args[0])

    startingdir = os.path.abspath(os.curdir)

    for d in questions:
        elapsed = ''
        note = ''
        
        os.chdir(os.path.join(startingdir, d))
        question = imp.load_source(d, d + '.py')

        if hasattr(question, 'expected'):
            print d,
            start = datetime.datetime.now()
            result = question.solve()
            end = datetime.datetime.now()
            elapsed = end-start
            if question.expected == result:
                label = 'PASS'
                if elapsed > datetime.timedelta(minutes=1):
                    label = 'SLOW'
            else:
                label = 'FAIL'
                note = 'expected ' + repr(question.expected) + ' but got ' + repr(result)


        else:
            label = 'SKIP'

        if options.show_skip or label != 'SKIP':
            print '\r' + d, label, elapsed, note

if __name__ == '__main__':
    do_main(sys.argv[1:])
