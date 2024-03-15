# Box bound checking
#------------------------------------------------------------------------------
def check_box_bound(u,v):
    if v < u:# upper bound < lowerbound
        print('incompatible box bounds')
        return True #  Program should stop
    elif(u==v):
        print('degenerate box bound')
        return True #  Program should stop
    else:
        return False #  Program should runn