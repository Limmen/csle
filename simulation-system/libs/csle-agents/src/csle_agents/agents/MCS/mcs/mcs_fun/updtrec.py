#------------------------------------------------------------------------------
def updtrec(j,s,f, record):
    '''
        % Input:
        % j           label of a box
        % s           its level
        % f           vector containing the base vertex function values of the
        %             already defined boxes
        % updates the pointer record(s) to the best non-split box at level s
        #global record      % record list
    '''
    if len(record) < s:
        record[s] = j
    elif record[s] == 0:
        record[s] = j
    elif f[j] < f[record[s]]:
        record[s] = j
        
    #print(j,s,record[s])
    return record