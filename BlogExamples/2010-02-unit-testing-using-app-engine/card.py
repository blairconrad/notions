#!/usr/bin/env python

from google.appengine.ext import db

class Card(db.Model):
    #family = db.ReferenceProperty(Family)
    number = db.StringProperty()
    name = db.StringProperty()
    pin = db.StringProperty()
    # library = db.ReferenceProperty(Library)

    def pin_is_valid(self):
        return self.pin != ''
    
