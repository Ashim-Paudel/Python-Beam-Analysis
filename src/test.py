from beamframe.beam import *

b = Beam(5, ndivs=10000)
ra = Reaction(0, 'h', 'A')
rb = Reaction(5, 'r', 'A')
p = PointLoad(2.5, 5, inverted=True)

b.fast_solve((ra, rb, p))
b.generate_graph(which='bmd', details=True)