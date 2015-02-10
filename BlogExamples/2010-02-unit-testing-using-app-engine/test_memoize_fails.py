#!/usr/bin/env python


import sys
import dev_appserver
sys.path = dev_appserver.EXTRA_PATHS + sys.path 

from google.appengine.api import memcache
from gael.memcache import *

def test_memoize_formats_string_key_using_kwargs():
    values = [1, 2]
    @memoize('hippo%(animal)szebra', 100)
    def pop_it(animal):
        return values.pop()

    result = pop_it(animal='rabbit')
    assert 2 == result

    cached_value = memcache.get('hipporabbitzebra')
    assert 2 == cached_value
    
