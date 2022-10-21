#Phase-1: A simple OOP based program for simple beam solving:
from inspect import Attribute
from logging import raiseExceptions
import math
import re
from typing import Iterable
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy.plotting.plot import Plot


"""
# About Beam library:
A beam is a structural element that primarily resists loads applied laterally to the beam's axis.
Its mode of deflection is primarily by bending.

This library has several class and their methods in order to solve a 2d Beam numerically and do beam analysis.

## Sign Conventions:
Positive x-axis for beam: increases in right hand side
Positive y-axis for beam: increases upward direction
Positive angle direction: Counter clockwise with respect to beam positive x-axis
Positive moment: Counter clockwise

## Units Conventions:
Length: meter
Angle: degrees
Load: kN
Moment: kNm
"""

class Beam:
    """
        `Beam` is the main class to represent a beam object and perform various calculations.

        ## Attributes
        `length(float)`: length of a beam
        
        `kwargs`: Here are few optional keyword arguments
        - `E(float)` = Modulus of Elasticity of beam material 
        - `I(float)` = 2nd moment of area of the cross section of beam
    """
    #initial kwargs lists for simply supported beam
    simply_supported = ('Elasticity', 'MOA')

    def __init__(self,length:float, **kwargs):
        self.length = length
        self.E = kwargs.get('E') or kwargs.get('Elasticity') #modulus of elasticity of the material
        self.I = kwargs.get('I') or kwargs.get('MOA') #second moment of area

        self.supports = kwargs.get('supports')
        #self.reactions
        #variables initialization for beam:
        self.x, self.V_x, self.M_x = sp.symbols('x V_x M_x')

        #intitial fx,fy,moment
        self.fx = 0 #sp.symbols('fx') #total sum of horizontal force
        self.fy = 0 #sp.symbols('fy') #total sum of vertical force
        self.m = 0 #sp.symbols('m') #total sum of moments
    
        self.solved_rxns = None #initialize variable to store solved values for reactions
        self.mom_fn = 0 #initialize variable to store bending moment values in numpy array
        self.shear_fn = 0 #initialize variable to store shear values in numpy array

    def add_loads(self, load_list:object):
        """
        ### Description:
        Adds different load values and Reaction variables to generate symbolic expression of all loads
        This will add respective component of different netload values. 
        `self.fx: x-components` and 
        `self.fy: y-components`

        #### Arguments
        `load_list` = List or Tuples of various load objects like `PointLoad, UDL, Reaction`

        """
        for loadtype in load_list:
            if isinstance(loadtype, PointLoad): 
                self.fx += loadtype.load_x
                self.fy += loadtype.load_y
            
            if isinstance(loadtype, Reaction):
                if hasattr(loadtype, 'rx_var'):
                    self.fx += loadtype.rx_var
                    self.fy += loadtype.ry_var
                else:
                    self.fy += loadtype.ry_var

            if isinstance(loadtype, UDL):
                self.fy += loadtype.netload #adds net load value of udl object

    def add_moments(self, momgen_list:object, about:float=0):
        """
        ### Description
        Receives a list or tuple of `PointLoad`, `Reaction`, `UDL` or `PointMoment` objects.
        Adds the moment due to those objects about origin.

        #### Sign Convention: 
        Anticlockwise moment are positively added. So, positive forces will give anticlockwise moments.

        #### Arguments and terms:
        - `momgen_list` = List or Tuples of various moment generators like `PointLoad, UDL, Reaction, PointMoment`
        - `about = 0`= Take moment about that x-coordinate in beam. `Default = 0, range = (0, self.length)`
        - `mom_gen(local variable)` = One which is capable of generating moment.
        """
        for mom_gen in momgen_list:  #takes moment about origin and adds up
            if isinstance(mom_gen, PointLoad):
                self.m += (mom_gen.pos-about)*mom_gen.load_y
            elif isinstance(mom_gen, Reaction):
                self.m += (mom_gen.pos-about)*mom_gen.ry_var
                if hasattr(mom_gen, 'mom_var'):
                    self.m += mom_gen.mom_var
            elif isinstance(mom_gen, PointMoment):
                self.m += mom_gen.mom
            elif isinstance(mom_gen, UDL):
                self.m += (mom_gen.netpos-about)*mom_gen.netload

    def calculate_reactions(self, reaction_list:object):
        """
        ### Description
        1. Generates 3 equations of static equilibrium: `self.fx=0 , self.fy=0,  self.m=0`.
        2. Uses `sympy.solve` to solve for symbolic variables `'rx_var', 'ry_var', 'mom_var'` in those equations. 
        3. Assign those values for unknown value of reactions object: `rx_val, ry_val, mom_val`.

        #### Arguments
        List or tuple of unknown reaction objects
        """
        Fx_eq = sp.Eq(self.fx,0)
        Fy_eq = sp.Eq(self.fy,0)
        M_eq = sp.Eq(self.m, 0)

        eval_values = [] #initialize an empty list to contain reactions variables to be solved
        possible_rxn = ['rx_var', 'ry_var', 'mom_var']
        possible_values = ['rx_val', 'ry_val', 'mom_val']
        for rxn_obj in reaction_list:
            for rxn_var in possible_rxn:
                if hasattr(rxn_obj, rxn_var):
                    eval_values.append(getattr(rxn_obj, rxn_var))
        print(eval_values)
        self.solved_rxns = sp.solve([Fx_eq, Fy_eq, M_eq], eval_values)

        #now assign values to the reaction objects too:
        for rxn_obj in reaction_list:
            for (rxn_val,rxn_var) in zip(possible_values, possible_rxn):
                if hasattr(rxn_obj, rxn_var):
                    setattr(rxn_obj, rxn_val, self.solved_rxns[getattr(rxn_obj, rxn_var)])

    def generate_moment_equation(self, loads:object):
        """
        ### Description
        1. Generates Macaulay's Equation for Moment due to various moment generators
        2. Assigns symbolic expression of BM to `self.mom_fn` attribute 
        3. Reassigns lambdified expression of BM to `self.mom_fn`
        4. Reassigns `numpy.vectorize()` expression to `self.mom_fn`

        #### Arguments
        List or Tuple of various moment generating objects:`PointLoad`, `Reaction`, `UDL` or `PointMoment`
        """
        for mom_gen in loads:
            if isinstance(mom_gen, PointLoad):
                self.mom_fn += mom_gen.load_y*sp.SingularityFunction('x', mom_gen.pos, 1)
            elif isinstance(mom_gen, Reaction):
                self.mom_fn += mom_gen.ry_val*sp.SingularityFunction('x', mom_gen.pos, 1)
                if hasattr(mom_gen, 'mom_val'):
                    self.mom_fn -= mom_gen.mom_val*sp.SingularityFunction('x', mom_gen.pos, 0)
            elif isinstance(mom_gen, PointMoment):
                self.mom_fn -= mom_gen.mom*sp.SingularityFunction('x', mom_gen.pos, 0)
                #because we have defined anticlockwise moment positive in PointMoment
            elif isinstance(mom_gen, UDL):
                self.mom_fn += mom_gen.loadpm*sp.SingularityFunction('x', mom_gen.start, 2)/2
                if mom_gen.end < self.length:
                    self.mom_fn -= mom_gen.loadpm*sp.SingularityFunction('x', mom_gen.end, 2)/2
        
        #in order to lambdify moment_equation and vectorize it:
        self.mom_fn = sp.lambdify(self.x, self.mom_fn, 'sympy')
        self.mom_fn =  np.vectorize(self.mom_fn)

    def generate_shear_equation(self, loads):
        """
        ### Description
        1. Generates Macaulay's Equation for Shear Force due to various force generators
        2. Assigns symbolic expression of ShearForce to `self.shear_fn` attribute 
        3. Reassigns lambdified expression of ShearForce to `self.shear_fn`
        4. Reassigns `numpy.vectorize()` expression to `self.shear_fn`

        #### Arguments
        List or Tuple of various force generating objects:`PointLoad`, `Reaction`, `UDL` 
        """
        for force_gen in loads:
            if isinstance(force_gen, PointLoad):
                self.shear_fn += force_gen.load_y*sp.SingularityFunction('x', force_gen.pos, 0)
            elif isinstance(force_gen, Reaction):
                self.shear_fn += force_gen.ry_val*sp.SingularityFunction('x', force_gen.pos, 0)
            elif isinstance(force_gen, UDL):
                self.shear_fn += force_gen.loadpm*sp.SingularityFunction('x', force_gen.start, 1)
                if force_gen.end < self.length: #add udl in opposite direction
                    self.shear_fn -= force_gen.loadpm*sp.SingularityFunction('x', force_gen.end, 1)

        self.shear_fn = sp.lambdify(self.x, self.shear_fn, 'sympy')
        self.shear_fn = np.vectorize(self.shear_fn)

class Load:
    '''
    Load class 

    ### Attributes:
    `pos(float)`: `unit:meter` position of that netload with respect to beam coordinates's origin
    `load(float)`: `unit:kN` net load of that load type(for point load that is point load value, 
                            but it will be different 
                            for other loads like uvl and udl)
    `inverted(bool)=False`: Default direction of positive net load is in positive direction of y-axes
    - by default: `inverted = False` (load is facing upward)
    - use `inverted=True` to indicate load is in downward direction

    '''

    def __init__(self, pos:float, load:float, inverted=False, **kwargs):
        self.pos = pos
        self.inverted = inverted
        if self.inverted:
            self.load = -1*load
        else:
            self.load = load
    

class PointLoad(Load):
    """
    ## Description 
    Subclass of Class Load

    ### Attributes:
    `pos, load, inverted`: inherit from super class `Load`
    `inclination(float)=90`: `unit=degree` represents angle made by direction of net load with positive direction of beam's x axis
                            inclination will be positive for counter clockwise direction
                            put negative inclination if you want to take angle in clockwise direction
    `load_x`: component of net load value in positive direciton of beam's x-axis
    `load_y`: component of net load value in positive y-direciton(upward direction)
    """

    def __init__(self, pos:float, load:float, inverted:bool=False, inclination=90, **kwargs):
        super().__init__(pos, load, inverted, **kwargs)
        #self.var = sp.symbols(var) #might require variable for load too.
        self.inclination = inclination  #inclination of point load with positive direction of beam axis
        self.load_x = round(self.load*np.cos(self.inclination*np.pi/180), ndigits=4)
        self.load_y = round(self.load*np.sin(self.inclination*np.pi/180), ndigits=4)

class UDL:
    """
    ## Description
    UDL is type of load that is combinaiton of infinite points load over certain length acting transverse to beam

    ### Attributes:
    `start(float)`:Start position of UDL
    `loadpm(float)`: Load Per meter of udl
    `span(float)`: Total length of udl
    `inverted(bool) = True`: UDL facing downwards on beam,
                                use `inverted=False` for upside udl
    `self.netload(float)`: total effective load of udl
    `self.netpos(float)`: position of effective load from beam origin
    """
    def __init__(self, start:float, loadpm:float, span:float, inverted:bool=True, **kwargs):
        self.start = start #x coordinate of left edge of udl
        self.span = span #total length of udl
        self.end = start + span
        self.inverted = inverted
        if self.inverted:
            self.loadpm = -1*loadpm
        else:
            self.loadpm = loadpm
        
        self.netload = self.loadpm * self.span #netload of udl
        self.netpos = self.start + self.span/2 #position of effective load of udl


class Reaction():
    """
    ## Description
        Reactions are given by supports. 3 types of supports are defined for now
        `hinge`, `roller` and `fixed` support.

    ### Attributes
    `pos(float)`: position of reaction
    `type(string)`: `'roller'`,`'hinge'`,`'fixed'` or `'r'`,`'h'`,`'f'`
    `rx_val, ry_val, mom_val`: variables to store numerical values for reaction loads and moments
    `rx_var, ry_var, mom_var`: symbolic variable to store symbolic values for reactions
    """
    def __init__(self, pos, type:str, pos_sym):
        self.pos = pos
        #possible reaction values(initialize them as zeros):
        self.rx_val = 0
        self.ry_val = 0
        self.mom_val = 0

        self.type = type.lower()
        if self.type == 'roller' or self.type == 'r':
            self.ry_var = sp.Symbol(f"R_{pos_sym}_y") #symbolic variable for that roller support
        elif self.type == 'hinge' or self.type == 'h':
            self.rx_var = sp.Symbol(f"R_{pos_sym}_x")
            self.ry_var = sp.Symbol(f"R_{pos_sym}_y")
        elif self.type == 'fixed' or self.type == 'f':
            self.rx_var = sp.Symbol(f"R_{pos_sym}_x")
            self.ry_var = sp.Symbol(f"R_{pos_sym}_y")
            self.mom_var = sp.Symbol(f"M_{pos_sym}")
        else:
            raise NameError(f"Unidentified support type: {self.type}")

class PointMoment():
    """
    ## Description
    Pure moment that act at point

    ### Attributes
    `pos`: location of that point moment from beam's origin
    `mom`: value of that point moment
    `ccw`(bool)=`False` : counterclockwise direciton is positive value of moment, 
                by defalut: ccw=False and given moment is positive
    
    """
    def __init__(self, pos, mom, ccw=True):
        self.pos = pos
        self.ccw = ccw
        if self.ccw:
            self.mom = mom
        else:
            self.mom = -1*mom





