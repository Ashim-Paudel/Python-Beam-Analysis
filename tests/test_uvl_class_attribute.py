from pibeam import *

uvl = UVL(start=0, startload=0, span=3, endload=4) #triangular load (inverted)
uvl2 = UVL(start=0, startload=4, span=3, endload=0)
uvl3 = UVL(start=2, startload=2, span=5, endload=4) #trapezoidal load(inverted)
uvl4 = UVL(start=2, startload=2, span=5, endload=4, inverted=False) #trapezoidal load (upright)


print(uvl.tload, uvl.rload)
print(uvl.netload, uvl.pos)

print(uvl2.tload, uvl2.rload)
print(uvl2.netload, uvl2.pos)

print(uvl3.tload, uvl3.rload)
print(uvl3.netload, uvl3.pos)


print(uvl4.tload, uvl4.rload)
print(uvl4.netload, uvl4.pos)