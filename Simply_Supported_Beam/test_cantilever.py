# question: https://civilengineeronline.com/mech/fig51a.gif
# solution : https://civilengineeronline.com/mech/fig51bsfbm.gif
# last question from figure
from beam import *

b = Beam(4)
rd = Reaction(b.length, 'f', 'D')
#rb = Reaction(b.length, 'f', 'B')
udl = UDL(1,4,2)
p = PointLoad(0, 2, inverted=True)
b.add_loads([rd, udl, p])
b.add_moments([rd, udl, p])
print(b.fx, b.fy, b.m)
print(b.solved_rxns)
b.calculate_reactions((rd,))
print(rd.rx_val, rd.ry_val, rd.mom_val)
b.generate_moment_equation([rd, udl, p])
b.generate_shear_equation((rd, udl, p))

x = np.linspace(-0.009, b.length, 1000)
plt.rc('font', family='serif', size=14)
fig, ax = plt.subplots(facecolor='w', edgecolor='w')
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
