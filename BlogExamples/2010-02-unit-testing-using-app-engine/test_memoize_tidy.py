#!/usr/bin/env python


import gael.testing
gael.testing.add_appsever_import_paths()
gael.testing.initialize_service_apis()

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
    
