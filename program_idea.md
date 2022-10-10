# Beam Analysis Module with python
## Problem Statement:

1. **What is Beam?** 
        A horizontal structural member used to safely carry and transfer loads through support to the ground.

2. **What we do on Beam analysis?**
        We compute all the support reactions and moments developed and find shear forces, bending moment and deflections at various points of the beam. 

3. **What I am aiming to build?**
        A library with all the Classes, Methods and Functions that could eventually create a beam model(numerical/ of equations) in python. 
        After certain goal completion this module will be made publicly available in github and other people will also be allowed to contribute and use this module to solve beam problems.

## Functionality and Structure
**Bold** Required arguments
*Italic* Optional arguments/attributes
| Class | Attributes | Methods | Remarks
| -- |- | -| - |
**Beam** | **length, supports,** $\\$ *Cross Sections (Standard T-section, L-section or Square or Rectangle) or Moment of Inertia $\\$ Modulus of Rigidity or Material Type(Steel, Iron etc.)* | Calculate Reactions, Axial Force, Shear Force and Bending moment at each point of beam | -
|
**Load** $\\$ SuperClass |  **position , load, inverted=False** | Moment due to that load about certain point on beam | $\\$ If Position is a single integer: That is the position, except a tuple with `(start_x, span_length)` $\\$ By default `inverted = false` meaning, load will be acting in downward direction.
|
**PointLoad** | **inherit, net_load**$\\$ *Angle of inclination with beam axis: Default= $90^{\circ}$* | Inherit | Subclass of Load
|
**UDL** | **inherit, net_load** | inherit | subclass of load
|
**UVL** | **inherit, net_load** | inherit | subclass of load
| **PointMoment** | **position, moment** | - | - 
| **Reaction** | **postion, direction, rxn_load, rxn_mom = None** | moment_due_reaction | super class
| **R_x** | **inherit** | inherit | sub class of reaction
|
**Diagram** | equation, **kwargs | afd, bmd, sfd, deflection, save_diagram | -
|



        