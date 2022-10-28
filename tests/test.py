from beam import *

b = Beam(14)
ra = Reaction(0, 'f', 'A')
p1 = PointLoad(2,100, inverted=True, inclination=90)
m1 = PointMoment(4,60, ccw=False)
h = Hinge(6, side='r')
udl = UDL(6,20,8)
re = Reaction(10, 'r', 'F')

elements = (udl, p1, m1, ra, re)
b.add_loads(elements)
b.add_moments(elements, about=3.5)
b.add_hinge(h, elements)
b.calculate_reactions((ra,re))
b.generate_moment_equation(elements)
b.generate_shear_equation(elements)


x = np.linspace(-1, b.length, 1000)
plt.rc('font', family='serif', size=14)
fig, ax = plt.subplots(facecolor='w', edgecolor='w', num="BMD vs SFD")
ax.plot(x, b.mom_fn(x), label="BMD (kNm)")
ax.plot(x, b.shear_fn(x), label="SFD (kN)")
ax.set_xticks(np.arange(0, b.length+1,1))
ax.axhline(y=0, color='k', label='beam')
ax.set_title("BMD vs SFD of Beam\n ")
ax.set_xlabel("x (m)")
ax.legend(fontsize=8)
ax.grid()
plt.savefig(f"Simply_Supported_Beam/generated_images/{__file__.split('/')[-1]}.png", dpi=500)
plt.show()