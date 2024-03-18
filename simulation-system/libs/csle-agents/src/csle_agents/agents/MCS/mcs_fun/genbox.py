
    
#------------------------------------------------------------------------------
def genbox(par,level0,nchild,f0):
    ipar = par #  set parent box index
    level = level0 #  set level value of the box
    ichild = nchild #  set number of child
    f = f0 # set optimal value of the box
    return ipar,level,ichild,f