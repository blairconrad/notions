#!/usr/bin/env python

from card import Card

def test_card_blank_pin_is_invalid():
    c = Card()
    c.pin = ''
    assert not c.pin_is_valid()
