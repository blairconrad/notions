#!/usr/bin/env python


import gael.testing
gael.testing.add_appsever_import_paths()
gael.testing.initialize_service_apis()

from gael.memcache_class import *

class MyCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key, None)

    def set(self, key, value, *args):
        print 'saving', value, 'in', key
        print 'extra args', args
        self.cache[key] = value

def test_memoize_formats_string_key_using_kwargs():
    values = [1, 2]
    @memoize('hippo %(animal)s zebra', 100)
    def pop_it(animal):
        return values.pop()

    cache = MyCache()
    pop_it.cache = cache
    result = pop_it(animal='rabbit')
    assert 2 == result

    cached_value = cache.get('hippo rabbit zebra')
    assert 2 == cached_value
    
def test_memoize_formats_string_key_using_kwargs2():
    values = [1, 2]
    @memoize('%(animal)s zebra', 100)
    def pop_it(animal):
        return values.pop()

    cache = MyCache()
    pop_it.cache = cache
    result = pop_it(animal='rabbit')
    assert 2 == result

    cached_value = cache.get('rabbit zebra')
    assert 2 == cached_value
    
