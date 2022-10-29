from pibeam import *

b = Beam(8)

ra = Reaction(0, 'h', 'A')
rb = Reaction(b.length, 'r', 'B')
uvl1 = UVL(0,0, 4, 4, inverted=False)
uvl2 = UVL(4,4,4,0)

loads = (ra, rb, uvl1, uvl2)

b.fast_solve(loads)
b.generate_graph()