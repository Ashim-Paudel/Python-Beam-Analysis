#question: https://ars.els-cdn.com/content/image/3-s2.0-B9780081025864000032-f03-22-9780081025864.jpg

from beam import *

b = Beam(4)
p1 = PointLoad(1,2,True)
p2 = PointLoad(2,5,True)
udl = UDL(3,4,1)
r_a = Reaction(0,'h','A')
r_e = Reaction(b.length, 'r', 'E')

b.add_loads((p1,p2, udl, r_a, r_e))
b.add_moments((p1,p2, udl, r_a, r_e), about=b.length)
b.calculate_reactions((r_a, r_e))
b.generate_moment_equation((p1,p2, udl, r_a, r_e))
b.generate_shear_equation((p1,p2, udl, r_a, r_e))

x = np.linspace(-0.009, b.length, 1000)
plt.rc('font', family='serif', size=14)
fig, ax = plt.subplots(facecolor='w', edgecolor='w', num="BMD vs SFD")
ax.plot(x, b.mom_fn(x), label="BMD (kNm)")
ax.plot(x, b.shear_fn(x), label="SFD (kN)")
ax.set_xticks(np.arange(0, b.length+1,1))
ax.axhline(y=0, color='k', label='beam')
ax.set_title("BMD vs SFD of Beam")
ax.set_xlabel("x (m)")
ax.legend()
ax.grid()
#plt.savefig("Simply_Supported_Beam/generated_images/test_question.png")
plt.show()