#------------------------------------------------------------------------------
def chrelerr(fbest,stop):
    fglob = stop[1]
    if fbest - fglob <= max(stop[0]*abs(fglob), stop[2]):
        flag = 0
    else:
        flag = 1
    
    return flag

#------------------------------------------------------------------------------
def chvtr(f,vtr):
    if f <= vtr:
        flag = 0
    else:
        flag = 1
        
    return flag



















