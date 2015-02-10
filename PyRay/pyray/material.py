#!/usr/bin/env python

class Material:
    def __init__(self, colour = (0,0,1.0), specularExponent = 0, specularColour = (0,0,1.0) ):
        self.colour = colour
        self.specularExponent = specularExponent
        self.specularColour = specularColour
