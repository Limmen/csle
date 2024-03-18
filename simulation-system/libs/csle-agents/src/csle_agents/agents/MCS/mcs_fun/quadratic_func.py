
#------------------------------------------------------------------------------
def quadmin(a,b,d,x0):
    if d[2] == 0:
        if d[1] > 0:
            x = a
        else:
            x = b
    elif d[2] > 0:
        x1 = 0.5*(x0[0] + x0[1]) - 0.5*d[1]/d[2]
        if a <= x1 and x1 <= b:
            x = x1
        elif quadpol(a,d,x0) < quadpol(b,d,x0):
            x = a
        else:
            x = b
    else:
        if quadpol(a,d,x0) < quadpol(b,d,x0):
            x = a
        else:
            x = b
    return x


#------------------------------------------------------------------------------
def quadpol(x,d,x0):
    '''
        evaluates the quadratic polynomial
    '''
    return d[0] + d[1]*(x - x0[0]) + d[2]*(x - x0[0])*(x - x0[1])