from beam import *

b = Beam(10)
ra = Reaction(0, 'r', 'A')
rb = Reaction(b.length, 'h', 'B')
udl = UDL(2, 10, b.length-2)
b.add_loads([ra, rb, udl])
b.add_moments([ra, rb, udl])
b.calculate_reactions([ra, rb])
b.generate_moment_equation([ra, rb, udl])
b.generate_shear_equation((ra, rb, udl))

print(b.fx, b.fy, b.m)
print(b.solved_rxns)
x = np.linspace(0, b.length, 1000)
plt.plot(x, b.mom_fn(x))
plt.plot(x, b.shear_fn(x))
plt.show()