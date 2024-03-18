import numpy as np
#------------------------------------------------------------------------------
def polint(x,f):
    '''
     quadratic polynomial interpolation
     args: 
         x(1:3)  3 pairwise distinct support points
         f(1:3)  corresponding function values
    return:
        d(1:3)  the interpolating polynomial is given by
    '''
    d = np.zeros(3)
    d[0] = f[0]
    d[1] = (f[1] - f[0])/(x[1] - x[0])
    f12 = (f[2] - f[1])/(x[2] - x[1])
    d[2] = (f12 - d[1])/(x[2] - x[0])
    return d


def polint1(x,f):
    '''
        quadratic polynomial interpolation
    '''
    f13 = (f[2]-f[0])/(x[2]-x[0])
    f12 = (f[1]-f[0])/(x[1]-x[0])
    f23 = (f[2]-f[1])/(x[2]-x[1])
    
    g = f13 + f12 - f23
    G = 2*(f13-f12)/(x[2]-x[1])
    return g,G