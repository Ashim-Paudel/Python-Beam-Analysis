from beamframe import *
from beamframe.beam import *

b = Beam(6)
uvl1 = UVL(0,3,3,0, inverted=True)
uvl2=UVL(3,0,3,3, inverted=False)
ra = Reaction(0,'h', 'A')
rb = Reaction(b.length, 'r','B')

loads = (uvl1, uvl2, ra, rb)
b.fast_solve(loads)
b.generate_graph(which='both', details=True)
