# Beam
A beam is a structural element that primarily resists loads applied laterally to the beam's axis (an element designed to carry primarily axial load would be a strut or column). Its mode of deflection is primarily by bending. The loads applied to the beam result in reaction forces at the beam's support points. The total effect of all the forces acting on the beam is to produce shear forces and bending moments within the beams, that in turn induce internal stresses, strains and deflections of the beam.
*Source: [Wikipedia](https://en.wikipedia.org/wiki/Beam_(structure))*



# Documentation
Version:  0.0.1

## Classes and their arguments:

| class | required arguments | optional arguments |
| -- | -- | -- |
| `Beam` | `length: float` | `E`,`I` |
| `Load` | `pos: float, load: float` | `inverted:bool=False` |
| `PointLoad` | `pos: float, load: float` | `inverted:bool = False, inclination:float=90` |
| `UDL`|  `start: float, loadpm: float, span: float` | `inverted:bool = True` |
| `UVL`| ` start: float, startload: float, span: float, endload: float` | `inverted: bool = True` |
| `Reaction` | `pos: float, type: str, pos_sym: str` | none |
| `PointMoment` | `pos: float, mom: float` | `ccw: bool = True` |
| `Hinge` | `pos: float` | `side: str = 'l'` |



