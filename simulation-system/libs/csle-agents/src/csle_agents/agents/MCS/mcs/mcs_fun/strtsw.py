import numpy as np
#------------------------------------------------------------------------------
def strtsw(smax, level, f, nboxes, record):
    '''
    # global nboxes record
    % nboxes - number of boxes not in the `shopping basket'
    % record(1:smax-1)  vector pointing to the best non-split box at each
    %              level; record(s) = 0 if there is no non-split box at 
    %              level s (record list)
    '''
    #% initialization
    record = np.zeros(smax).astype(int)
    s = smax
    for j in range(nboxes+1):
        # recording non-split boxes
        if level[j] > 0: # level denoted  0 < s < smax 
            if level[j] < s:
                s = level[j] # assigning level 
                
            if not record[level[j]]:
                record[level[j]] = j
                #print('for ',level[j],j)
            elif f[j] < f[record[level[j]]]:
                record[level[j]] = j
                #print(level[j],j)
    return s, record