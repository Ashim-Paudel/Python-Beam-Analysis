from beamframe import *

b = Beam(10)
ra = Reaction(0, 'r', 'A')
rb = Reaction(b.length, 'h', 'B')
udl = UDL(0, 10, 5)
b.add_loads([ra, rb, udl])
b.add_moments([ra, rb, udl], about=b.length)
b.calculate_reactions([ra, rb])
b.generate_moment_equation([ra, rb, udl])
b.generate_shear_equation((ra, rb, udl))

print(b.fx, b.fy, b.m)
print(b.solved_rxns)

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
#plt.savefig("Simply_Supported_Beam/generated_images/test_question.png")
plt.show()