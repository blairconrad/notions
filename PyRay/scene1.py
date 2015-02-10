#!/usr/bin/env python

import pyray
import sys
from pyray.material import Material

pyray.superSampleLevel = 2 

scene = (
    pyray.Sphere((-1, 0.2, 0), 1),
    pyray.Sphere((1, 0, 0), 1.3),
    #pyray.Sphere((0,0.5,0),.8)
    )
scene[0].material = Material((1.0, 0, 0))
scene[1].material = Material((0, 0, 1.0))

pyray.render(sys.argv[1], scene)
