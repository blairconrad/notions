#!/usr/bin/env python

import logging
import google.appengine.api.memcache


def memoize(key, seconds_to_keep=600):
    '''Use the memcache to memoize the result of invoking a
    callable. Returns a function that will check to see if a result is
    stored in the memcache. If not, it will call the original function
    and store the result in the memcache for seconds_to_keep seconds.

    If key is callable, the key string used to identify the results in
    the memcache is equal to key(args, kwargs), where *args and
    **kwargs are the arguments to the decorated function. Otherwise,
    the key is treated as a format string and evaluated as
    (key % kwargs).
    ''' 
    def decorator(func):
        def wrapper(*args, **kwargs):
            if callable(key):
                key_value = key(args, kwargs)
            else:
                key_value = key % kwargs

            cached_result = google.appengine.api.memcache.get(key_value)
            if cached_result is not None:
                logging.debug('found ' + key_value)
                return cached_result
            logging.info('calling func to get '  + key_value)
            result = func(*args, **kwargs)
            google.appengine.api.memcache.set(key_value, result, seconds_to_keep)
            return result
        return wrapper
    return decorator
        
