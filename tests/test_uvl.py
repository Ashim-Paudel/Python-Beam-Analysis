from beamframe import *

b = Beam(10)
uvl = UVL(0,0, b.length,10)
ra = Reaction(0,'f', 'A')
print(uvl.netload)
print(uvl.netload*uvl.pos)
print(uvl.gradient)
b.add_loads((uvl, ra))
b.add_moments((uvl, ra))
b.calculate_reactions((ra,))
b.generate_shear_equation((uvl, ra))

x = np.linspace(-1, b.length, 500)
plt.rc('font', family='serif', size=14)
fig, ax = plt.subplots(facecolor='w', edgecolor='w', num="BMD vs SFD")
#ax.plot(x, b.mom_fn(x), label="BMD (kNm)")
ax.plot(x, b.shear_fn(x), label="SFD (kN)")
ax.set_xticks(np.arange(0, b.length+1,1))
ax.axhline(y=0, color='k', label='beam')
ax.set_title("BMD vs SFD of Beam")
ax.set_xlabel("x (m)")
ax.legend(fontsize=8)
ax.grid()
#plt.savefig(f"Simply_Supported_Beam/generated_images/{__file__.split('/')[-1]}.png")
plt.show()