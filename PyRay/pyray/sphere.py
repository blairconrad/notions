#!/usr/bin/env python

import math
import intersection
import vector

def subVector(vector1, vector2):
    return map(lambda x, y: x-y, vector1, vector2)
    
class Sphere:
    def __init__(self, origin=(0,0,0), radius=1):
        self.origin = origin
        self.radius = radius
        
    def allIntersections(self, ray):
        results = []
        origin = (ray[0][0] - self.origin[0],
                  ray[0][1] - self.origin[1],
                  ray[0][2] - self.origin[2])
        
        v = ray[1]
        c = origin[0]**2 + origin[1]**2 + origin[2]**2 - self.radius ** 2
        b = 2 * (origin[0] * v[0] + origin[1] * v[1] + origin[2] * v[2])
        a = v[0]**2 + v[1]**2 + v[2]**2
        inside = b**2 - 4* a * c 
        if inside >= 0:
            discrim = math.sqrt(inside)
            if -b - discrim > 0:
                intersectionDist = (-b-discrim)/2.0/a
                intersectionPoint = ((ray[0][0] + intersectionDist * v[0],
                                      ray[0][1] + intersectionDist * v[1],
                                      ray[0][2] + intersectionDist * v[2]))
                results.append(intersection.Intersection(intersectionDist, intersectionPoint,
                                                         subVector(intersectionPoint, self.origin),
                                                         self.material))
        return results

    def intersect(self, ray):
        return len(self.allIntersections(ray)) > 0
        

