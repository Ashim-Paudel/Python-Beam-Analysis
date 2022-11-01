"""
Module for singularity function

"""
def SingularityFunction(x:float, a:float, n:int):
    """
    Main singularity function definition
    """
    shift = float(x-a)
    exp = int(n)
    if isinstance(shift, complex):
        if not shift.imag == 0:
            raise ValueError("Singularity Functions are valid for real numbers only.")
    if isinstance(exp, complex):
        if not exp.imag == 0:
            raise ValueError("Singularity Functions are valid for real exponents only.")       
    if (exp + 2) < 0:
        raise ValueError("Singularity Functions are valid for exponents greater than -2 only.")
    if shift < 0:
        return 0
    elif shift >= 0:
        if exp < 0:
            return 0
        else:
            return shift**exp

            

            


        