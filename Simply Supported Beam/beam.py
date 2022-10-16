#Phase-1: A simple OOP based program for simple beam solving:
from turtle import position
import sympy as sp
import matplotlib.pyplot as plt

class Beam:
    """
        2d model of a Beam
        length: length of a beam

    
    """
    #initial kwargs lists for simply supported beam
    simply_supported = ('Elasticity', 'MOA')

    def __init__(self,length:float, **kwargs):
        self.length = length
        self.E = kwargs.get('E') or kwargs.get('Elasticity') #modulus of elasticity of the material
        self.I = kwargs.get('I') or kwargs.get('MOA') #second moment of area

        #variables initialization for beam:
        self.x, self.V_x, self.M_x = sp.symbols('x V_x M_x')

        #intitial fx,fy,moment
        self.fx = 0 #sp.symbols('fx') #total sum of horizontal force
        self.fy = 0 #sp.symbols('fy') #total sum of vertical force
        self.m = 0 #sp.symbols('m') #total sum of moments
    
    def sf(self,y,z):
        return sp.SingularityFunction(self.x,y,z)

    def add_load(self, load):
        if isinstance(load, PointLoad): 
            if load.inclination == 90 and load.inverted:
                self.fy += load.load
            

    
class Load:
    def __init__(self, pos:float, load:float, inverted=False, **kwargs):
        self.pos = pos
        self.inverted = inverted
        if self.inverted:
            self.load = -1*self.load
        else:
            self.load = load
    

class PointLoad(Load):
    def __init__(self, pos, load, inclination=90, **kwargs):
        super().__init__(self, pos, load, **kwargs)
        self.inclination = inclination  #inclination of point load with positive direction of beam axis

b = Beam(length=50, Elasticity=500)
up = PointLoad(pos=5, load=10)
down = PointLoad(pos=5, load=10, inverted=True)
print(up.load, down.load)
    



