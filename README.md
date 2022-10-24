# Beam
A beam is a structural element that primarily resists loads applied laterally to the beam's axis (an element designed to carry primarily axial load would be a strut or column). Its mode of deflection is primarily by bending. The loads applied to the beam result in reaction forces at the beam's support points. The total effect of all the forces acting on the beam is to produce shear forces and bending moments within the beams, that in turn induce internal stresses, strains and deflections of the beam.
*Source: [Wikipedia](https://en.wikipedia.org/wiki/Beam_(structure))*



# Documentation
Version:  0.0.1

## Classes and their arguments:

| class | required arguments | optional arguments |
| -- | -- | -- |
| `Beam` | `length: float` | `E: float, I:float` |
| `Load` | `pos: float, load: float` | `inverted:bool=False` |
| `PointLoad` | `pos: float, load: float` | `inverted:bool = False, inclination:float=90` |
| `UDL`|  `start: float, loadpm: float, span: float` | `inverted:bool = True` |
| `UVL`| ` start: float, startload: float, span: float, endload: float` | `inverted: bool = True` |
| `Reaction` | `pos: float, type: str, pos_sym: str` | none |
| `PointMoment` | `pos: float, mom: float` | `ccw: bool = True` |
| `Hinge` | `pos: float` | `side: str = 'l'` |


---

# Beam:
 `Beam` is the main class to represent a beam object and perform various calculations.

### Arguments 

`length(float)`: length of a beam

Here are few optional keyword arguments
- `E(float)` = Modulus of Elasticity of beam material 
- `I(float)` = 2nd moment of area of the cross section of beam

**Example**
```
# to create a beam of length 5m:
b = Beam(5)
```

---

# Load
### Arguments:
- `pos(float)`: position of that netload with respect to beam coordinates's origin
- `load(float)`: net load of that load type(for point load that is point load value, 
                        but it will be different 
                        for other loads like uvl and udl)
- `inverted(bool)=False`: Default direction of positive net load is in positive direction of y-axes
    - by default: `inverted = False` (Positive Load)
    - use `inverted=True` (indicates negative Load)

# PointLoad
### Description 
Subclass of class `Load`

### Arguments
- `pos, load, inverted`: inherit from super class `Load`
- `inclination(float)=90`: `unit=degree` represents angle made by direction of net load with positive direction of beam's x axis
    - inclination will be positive for counter clockwise direction
    - put negative inclination if you want to take angle in clockwise direction

### Attributes
- `load_x`: component of net load value in positive direciton of beam's x-axis
- `load_y`: component of net load value in positive y-direciton(upward direction)

# UDL
UDL(Uniformly Distributed Load) is type of load that is combinaiton of infinite points load over certain length acting transverse to beam
### Arguments:
- `start(float)`:Start position of UDL
- `loadpm(float)`: Load Per meter of udl
- `span(float)`: Total length of udl
- `inverted(bool) = True`: UDL facing downwards on beam
    - use `inverted=False` for upside udl
### Attributes
- `netload(float)`: total effective load of udl
- `pos(float)`: position of effective load from - beam origin

# UVL
It is that load whose magnitude varies along the loading length with a constant rate. 
Uniformly varying load is further divided into two types:

    1. Triangular Load
    2. Trapezoidal Load

### Arguments
- `start:float` = Start position of uvl from beam's origin along x-axis of beam coordinate system
- `startload:float` = `unit: kN/m` = Starting load/m value of uvl
- `span:float` = Total length of uvl object
- `endload:float` = Ending load/m value of uvl object
- `inverted:bool= True` : Default=`True` Inverts the uvl object

### Attributes
- `end` = End coordinate of uvl object
- `tload` = Net load value of upper triangular part of trapezoidal or triangular load
- `rload` = Net load value of lower rectangular part of trapezoidal load itself
- `netload` = Net load of whole uvl object itself. `netload = tload + rload`
- `netpos` = Net position(coordinates) where net load of uvl acts
 
# Reaction
Reactions are given by supports. 3 types of supports are defined for now: 
`hinge`, `roller` and `fixed` support.

### Arguments
- `pos(float)`: position of reaction
- `type(str)`: any one of `('roller'`,`'hinge'`,`'fixed')` or `('r'`,`'h'`,`'f')` Representing support condition at that point.
- `pos_sym(str)`: Symbolic variable to represent support location name 

### Attributes
- `rx_val, ry_val, mom_val`: variables to store numerical values for reaction loads and moments
- `rx_var, ry_var, mom_var`: symbolic variables to store symbolic values for reactions
 
# PointMoment
Pure moment that act at point

### Arguments
- `pos` : location of that point moment from beam's origin
- `mom` : value of that point moment
- `ccw(bool) = False` : counterclockwise direciton is positive value of moment, 
    - by defalut: `ccw = False` and given moment is positive

# Hinge
Internal hinges are provided in a structure to reduce statical indeterminacy of the structure. 
Bending moment at internal hinge is always zero. 
Internal hinge makes structure more flexible. 
It allows structure to move which reduces the reactive stresses.

### Arguments
- `pos:float` = Position of that internal hinge from origin of beam coordinate system
- `side:str = 'l'` : Accepted Values = `('r', 'right', 'l', 'left')`
    - Default Value = `'l'`
    - This side specifies which side of loads to take in order to take moment of that loads about hinge.

