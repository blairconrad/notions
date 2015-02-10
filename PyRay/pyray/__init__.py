#!/usr/bin/env python

import sys
import math
import Image

from sphere import Sphere
from plane import Plane
from intersection import Intersection
from material import Material
import vector

imageSize = (100, 75)
fieldOfView = math.radians(60/2.0) # degrees
eyePoint = (0, 0, -3)
dist = imageSize[0] / 2.0 / math.tan(fieldOfView)
ambientLight = (1, 1, 1)

superSampleLevel = 1
numRays = {}

# def render:
#    for each pixel
#        traceRay (or bunch of rays, to antialias)
#
# def traceRay:
#    findIntersection
#    if valid:
#       shade
#    else:
#       backgroundColour
#
# def findIntersection:
#    set up model, inverse model matrix, default material
#    traverse graph and return intersection point
#
# def traverse graph:
#    switch on object type, finding intersection point, normal, material
#    check all the children to see if they're closer
#
# def shade:
#    colour = component-wise multiplication of material & ambient
#    for each light:
#       if no obstruction:
#          attenuate, add stuff based on speculars and stuff
#          find out what colour comes from the reflections, sum them up

def backgroundColour():
    return (0,0,0)

def maxColourDifference(colours):
    max = 0.0
    for i in range(len(colours)):
        for j in range(i + i, len(colours)):
            for k in range(3):
                diff = abs(colours[i][k] - colours[j][k])
                if max < diff:
                    max = diff
    return max

def averageColours(colours):
    average = [0, 0, 0]
    for colour in colours:
        average[0] += colour[0]
        average[1] += colour[1]
        average[2] += colour[2]
    average[0] /= 1.0 * len(colours)
    average[1] /= 1.0 * len(colours)
    average[2] /= 1.0 * len(colours)

    return average

def findClosestIntersection(ray, scene):
    closestDist = 1000
    bestHit = None
    for thing in scene:
        hits = thing.allIntersections((eyePoint, ray))
        for hit in hits:
            if hit.distance < closestDist:
                bestHit = hit
                closestDist = bestHit.distance
    return bestHit
    

def shade(ray, intersection):
    """Find the colour at the intersection. Assumes ray is normalized"""
    lightStrength = -vector.dotProduct(vector.normalize(intersection.normal), ray)
    
    return (lightStrength * ambientLight[0] * intersection.material.colour[0],
            lightStrength * ambientLight[1] * intersection.material.colour[1],
            lightStrength * ambientLight[2] * intersection.material.colour[2])

def traceRay(center, scene):
    ray = (center[0], center[1], dist)
    ray = vector.normalize(ray)
    intersection = findClosestIntersection(ray, scene)

    if intersection:
        # shade
        colour = shade(ray, intersection)
    else:
        colour = backgroundColour()
    #print center, colour
    return colour
    
def traceArea(center, size, scene, level, maxLevel):
    if level == maxLevel:
        numRays[level] = numRays[level] + 1
        return traceRay(center, scene)
    else:
        # level < maxLevel... shoot four rays
        newCenters = ((center[0] - size[0]/4.0, center[1] - size[1]/4.0),
                      (center[0] - size[0]/4.0, center[1] + size[1]/4.0),
                      (center[0] + size[0]/4.0, center[1] - size[1]/4.0),
                      (center[0] + size[0]/4.0, center[1] + size[1]/4.0))
        colours = []
        
        for center in newCenters:
            # single ray
            numRays[level] = numRays[level] + 1
            colours.append(traceRay(center, scene))

        if level + 1 == maxLevel or maxColourDifference(colours):
            return averageColours(colours)
        else:
            # use the computed average colour, as well as the four new ones
            colours = [averageColours(colours)]
            newSize = (size[0]/2.0, size[1]/2.0)

            for center in newCenters:
                colours.append(traceArea(center, newSize, scene, level + 1, maxLevel))
                
            return averageColours(colours)

def mapColour(colour):
    def transformAndCap(value):
        return min(max(0, int(256 * value)), 255)
    return tuple(map(transformAndCap, colour))

def render(filename, scene):
    for num in range(superSampleLevel):
        numRays[num] = 0
    image = Image.new('RGB', imageSize)

    progressChunk = 10
    lastPercent = -1
    topLeft = (-imageSize[0]/2.0  + .5, imageSize[1]/2.0 - .5)

    # make sure every thing in the scene has a material
    for thing in scene:
        if not hasattr(thing, 'material'):
            thing.material = Material()
        
    for i in range(0, imageSize[0]):
        thisPercent = i/(imageSize[0]/(100/progressChunk)) * progressChunk
        if thisPercent != lastPercent:
            print '%2d%%' % (thisPercent,)
            lastPercent = thisPercent

        for j in range(0, imageSize[1]):
            pixelPos = (topLeft[0] + i, topLeft[1] - j)

            colour = traceArea(pixelPos, (1.0, 1.0), scene, 0, superSampleLevel)
            #print 'pixel:', (i,j), colour
            
            image.putpixel((i,j), mapColour(colour))

    print numRays
    image.save(filename)

    
