#!/usr/bin/env python

import math
import intersection
import vector

class Plane:
    def __init__(self, point, normal):
        self.normal = vector.normalize(normal)
        self.constant = - (self.normal[0] * point[0] + self.normal[1] * point[1] + self.normal[2] * point[2])

    def allIntersections(self, ray):
        results = []
        p = ray[0]
        v = ray[1]
        intersectionDist = - ( ( p[0] * self.normal[0]  
                                 + p[1] * self.normal[1]  
                                 + p[2] * self.normal[2]
                                 + self.constant ) /
                               ( v[0] * self.normal[0]  
                                 + v[1] * self.normal[1]  
                                 + v[2] * self.normal[2] ) )

        if intersectionDist >= 0:
            intersectionPoint = ((p[0] + intersectionDist * v[0],
                                  p[1] + intersectionDist * v[1],
                                  p[2] + intersectionDist * v[2]))
            
            normal = self.normal
            if vector.dotProduct(normal, v) > 0:
                normal = (-normal[0], -normal[1], -normal[2])
            results.append(intersection.Intersection(intersectionDist,
                                                     intersectionPoint,
                                                     normal,
                                                     self.material))
        return results

    def intersect(self, ray):
        return len(self.allIntersections(ray)) > 0
