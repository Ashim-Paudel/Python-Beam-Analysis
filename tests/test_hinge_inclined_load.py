from pibeam import *

# q:b -> https://learnaboutstructures.com/sites/default/files/images/3-Frames/Problem-4-1.png

b = Beam(16)
ra = Reaction(0, 'f', 'A')
h = Hinge(6)
p = PointLoad(10,117,inverted=True, inclination=53.1301024)
m = PointMoment(b.length, 65, ccw=False)
rd = Reaction(b.length, 'r', 'D')

b.add_loads((ra, p, rd))
b.add_moments((ra, p, m, rd))
b.add_hinge(h, (ra, p, rd))
b.calculate_reactions((ra,rd))
b.generate_moment_equation((ra, p, m,rd))
b.generate_shear_equation((ra, p, m,rd))


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