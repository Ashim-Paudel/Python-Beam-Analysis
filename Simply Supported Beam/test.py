from sympy.physics.continuum_mechanics.beam import Beam
from sympy import symbols, Piecewise
E, I = symbols('E, I')
R1, R2 = symbols('R1, R2')
b = Beam(4, E, I)
b.apply_load(R1, 0, -1)
b.apply_load(6, 2, 0)
b.apply_load(R2, 4, -1)
b.bc_deflection = [(0, 0), (4, 0)]
b.boundary_conditions
b.load
b.solve_for_reaction_loads(R1, R2)
b.load
b.shear_force()
b.bending_moment()
b.slope()
b.deflection()
b.deflection().rewrite(Piecewise)