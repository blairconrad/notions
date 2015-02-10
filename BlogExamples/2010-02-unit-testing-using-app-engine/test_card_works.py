#!/usr/bin/env python

import sys
import dev_appserver
sys.path = dev_appserver.EXTRA_PATHS + sys.path 

from card import Card

def test_card_blank_pin_is_invalid():
    c = Card()
    c.pin = ''
    assert not c.pin_is_valid()
