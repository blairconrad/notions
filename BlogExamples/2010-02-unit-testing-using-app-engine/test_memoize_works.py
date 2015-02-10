#!/usr/bin/env python


import sys
import dev_appserver
sys.path = dev_appserver.EXTRA_PATHS + sys.path 

from google.appengine.tools import dev_appserver

from google.appengine.tools.dev_appserver_main import ParseArguments
args, option_dict = ParseArguments(sys.argv) # Otherwise the option_dict isn't populated.
dev_appserver.SetupStubs('local', **option_dict)


from google.appengine.api import memcache
from gael.memcache import *

def test_memoize_formats_string_key_using_kwargs():
    values = [1, 2]
    @memoize('hippo %(animal)s zebra', 100)
    def pop_it(animal):
        return values.pop()

    result = pop_it(animal='rabbit')
    assert 2 == result

    cached_value = memcache.get('hippo rabbit zebra')
    assert 2 == cached_value
    
