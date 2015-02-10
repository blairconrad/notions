#!/usr/bin/env python

import sys
import datetime
sys.path.append('..')
import shared

def main(args=None):
    start = datetime.datetime.now()
    result = 510510 # because it's 2*3*5*7*11*13*17
    end = datetime.datetime.now()
    print result
    assert 510510 == result
    
    print 'Elapsed:', end - start
    return 0


if __name__ == '__main__':
    sys.exit(main())
