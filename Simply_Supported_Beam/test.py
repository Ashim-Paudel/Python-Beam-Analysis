from beam import *

b = Beam(5)
p = PointLoad(b.length/2, 10, inverted=True)
ra = Reaction(0, 'h', 'A')
rb = Reaction(5, 'r', 'B')

b.add_loads((p, ra, rb))
b.add_moments((p, ra, rb))
b.calculate_reactions((ra,rb))
b.generate_moment_equation((p,ra,rb))
b.generate_shear_equation((p,ra,rb))
b.generate_graph(which='both')