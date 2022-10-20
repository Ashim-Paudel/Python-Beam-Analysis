# question link: https://www.engineer4free.com/uploads/1/0/2/9/10296972/structural-analysis-tutorials_orig.png
# last question from figure
from beam import *

b = Beam(20)
ra = Reaction(0, 'f', 'A')
#rb = Reaction(b.length, 'f', 'B')
udl = UDL(10, 10, 10)
p = PointLoad(5, 50, inverted=True)
b.add_loads([ra, udl, p])
b.add_moments([ra, udl, p])
print(b.fx, b.fy, b.m)
print(b.solved_rxns)
b.calculate_reactions((ra,))
print(ra.rx_val, ra.ry_val, ra.mom_val)
b.generate_moment_equation([ra, udl, p])
b.generate_shear_equation((ra, udl, p))

x = np.linspace(0, b.length, 1000)
plt.plot(x, b.mom_fn(x))
plt.plot(x, b.shear_fn(x))
plt.show()
