from beam import *

b = Beam(6)
uvl1 = UVL(0,3,3,0)
uvl2 = UVL(3,0,3,3, inverted=False)
ra = Reaction(0, 'h', 'A')
rb = Reaction(6, 'r', 'B')

elem = (uvl1, uvl2, ra, rb)
b.add_loads(elem)
b.add_moments(elem)
b.calculate_reactions((ra, rb))
b.generate_shear_equation(elem)
b.generate_moment_equation(elem)
b.generate_graph('both')