from beamframe import *
# gbm book page: 28 qn 1
# test question form SOM book by GBM

b = Beam(11)
udl = UDL(0,10,4)
p1 = PointLoad(6,50, inverted=True)
m = PointMoment(6,50, ccw=False)
p2 = PointLoad(b.length, 80, inverted=True, inclination=30)
ra = Reaction(0, 'h', 'A')
rd = Reaction(8, 'r', 'D')

print(p1.load_x, p1.load_y)
print(p2.load_x, p2.load_y)

b.add_loads((udl, p1, p2, ra, rd))
b.add_moments((udl, p1, m, p2, ra, rd))
b.calculate_reactions((ra,rd))
b.generate_moment_equation((udl, p1, m, p2, ra, rd))
b.generate_shear_equation((udl, p1, p2, ra, rd))

x = np.linspace(-1, b.length, 1000)
plt.rc('font', family='serif', size=14)
fig, ax = plt.subplots(facecolor='w', edgecolor='w', num="BMD vs SFD")
ax.plot(x, b.mom_fn(x), label="BMD (kNm)")
ax.plot(x, b.shear_fn(x), label="SFD (kN)")
ax.set_xticks(np.arange(0, b.length+1,1))
ax.axhline(y=0, color='k', label='beam')
ax.set_title("BMD vs SFD of Beam")
ax.set_xlabel("x (m)")
ax.legend(fontsize=8)
ax.grid()
plt.savefig(f"Simply_Supported_Beam/generated_images/{__file__.split('/')[-1]}.png")
plt.show()