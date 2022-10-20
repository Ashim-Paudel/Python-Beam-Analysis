#Phase-1: A simple OOP based program for simple beam solving:
from inspect import Attribute
from logging import raiseExceptions
import math
import re
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

    def add_loads(self, load_list:list):
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
                self.fy += loadtype.netload

    def add_moments(self, load_list):
        """
        Receives a list of moment generators classes like: PointLoad,  Reaction, PointMoment
        """
        for mom_gen in load_list: 
            if isinstance(mom_gen, PointLoad):
                self.m += mom_gen.pos*mom_gen.load_y
            elif isinstance(mom_gen, Reaction):
                self.m += mom_gen.pos*mom_gen.ry_var
                if hasattr(mom_gen, 'mom_var'):
                    self.m += mom_gen.mom_var
            elif isinstance(mom_gen, PointMoment):
                self.m += mom_gen.mom
            elif isinstance(mom_gen, UDL):
                self.m += mom_gen.netpos*mom_gen.netload

    def calculate_reactions(self, reaction_list):
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

        self.solved_rxns = sp.solve([Fx_eq, Fy_eq, M_eq], eval_values)

        #now assign values to the reaction objects too:
        for rxn_obj in reaction_list:
            for (rxn_val,rxn_var) in zip(possible_values, possible_rxn):
                if hasattr(rxn_obj, rxn_var):
                    setattr(rxn_obj, rxn_val, self.solved_rxns[getattr(rxn_obj, rxn_var)])

    def generate_moment_equation(self, loads):
        for mom_gen in loads:
            if isinstance(mom_gen, PointLoad):
                self.mom_fn += mom_gen.load_y*sp.SingularityFunction('x', mom_gen.pos, 1)
            elif isinstance(mom_gen, Reaction):
                self.mom_fn += mom_gen.ry_val*sp.SingularityFunction('x', mom_gen.pos, 1)
            elif isinstance(mom_gen, PointMoment):
                self.mom_fn += mom_gen.mom*sp.SingularityFunction('x', mom_gen.pos, 0)
                #because we have defined anticlockwise moment positive in PointMoment
            elif isinstance(mom_gen, UDL):
                self.mom_fn += mom_gen.loadpm*sp.SingularityFunction('x', mom_gen.start, 2)/2
                if mom_gen.end < self.length:
                    self.mom_fn += mom_gen.loadpm*sp.SingularityFunction('x', mom_gen.start, 2)/2
        
        #in order to lambdify moment_equation and vectorize it:
        self.mom_fn = sp.lambdify(self.x, self.mom_fn, 'sympy')
        self.mom_fn =  np.vectorize(self.mom_fn)

    def generate_shear_equation(self, loads):
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

    def dummy_udl(self, udl):
        pass

    def show_graph(self):
        title = "Bending Moment Diagram"
        xlabel = "Beam Length"
        ylabel = "Moment(kNm)"
        xlim = (0, self.length)
        size = (10,7)
        sp.plot(self.mom_fn)

class Load:
    '''
    Load class 

    attributes:
    pos(m): position of that netload with respect to beam coordinates's origin
    load(kN): net load of that load type(for point load that is point load value, but it will be different 
    for other loads like uvl and udl)
    inverted(bool): default direction of positive net load is in positive direction of y-axes
                by default inverted = False (load is facing upward)
                use inverted=True to indicate load is in downward direction

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
    Subclass of Class Load

    Attributes:
    pos, load, inverted: inherit from super class
    var: symbolic variable for that load(useful in case of reactions)
    inclination(in degrees): angle made by direction of net load with positive direction of beam's x axis
                            inclination will be positive for counter clockwise direction
                            put negative inclination if you want to take angle in clockwise direction
    load_x: component of net load value in positive direciton of beam's x-axis
    load_y: component of net load value in positive y-direciton(upward direction)
    """

    def __init__(self, pos:float, load:float, inverted:bool=False, inclination=90, **kwargs):
        super().__init__(pos, load, inverted, **kwargs)
        #self.var = sp.symbols(var) #might require variable for load too.
        self.inclination = inclination  #inclination of point load with positive direction of beam axis
        self.load_x = round(self.load*np.cos(self.inclination*np.pi/180), ndigits=4)
        self.load_y = round(self.load*np.sin(self.inclination*np.pi/180), ndigits=4)

class UDL:
    
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
    Reaction class
    pos(float): position of reaction
    type(string): 'roller','hinge','fixed' or 'r','h','f'
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
    ## Attributes
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





