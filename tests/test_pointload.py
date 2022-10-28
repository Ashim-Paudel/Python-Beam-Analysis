from beam import *

b = Beam(length=10)
p = PointLoad(b.length/2, 10, True)
ra = Reaction(0, 'r', 'A')
rb = Reaction(b.length, 'h', 'B')
print(ra.ry_val, rb.rx_val, rb.ry_val)
b.add_loads((p,ra,rb))
b.add_moments((p,ra,rb), about=b.length)
print(b.fx, b.fy, b.m)
b.calculate_reactions((ra,rb))
print(b.solved_rxns)
print(b.solved_rxns[rb.ry_var])
print(ra.ry_val, rb.rx_val, rb.ry_val)
b.generate_moment_equation(loads=[p,ra,rb])
b.generate_shear_equation(loads=[p,ra,rb])
x = np.linspace(-1, b.length, 1000)
fig, ax = plt.subplots(figsize=(10,7))
ax.plot(x, b.mom_fn(x), label='BMD')
ax.plot(x,b.shear_fn(x), label="SFD")
ax.axhline(y=0, color='k', label='beam')
ax.legend()
plt.show()