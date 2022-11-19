from beamframe.beam import *

# q:b -> https://learnaboutstructures.com/sites/default/files/images/3-Frames/Problem-4-1.png

b = Beam(16)
ra = Reaction(0, 'f', 'A')
h = Hinge(6)
p = PointLoad(10,117,inverted=True, inclination=53.1301024)
m = PointMoment(b.length, 65, ccw=False)
rd = Reaction(b.length, 'r', 'D')

b.fast_solve((ra, h, p, m, rd))
b.save_data("test_data")