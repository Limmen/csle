def neighbor(x,delta,u,v):
    '''
        computes 'neighbors' x1 and x2 of x needed for making triple search 
        and building a local quadratic model such that x(i), x1(i), x2(i) are
        pairwise distinct for i = 1,...,n
    '''
    i1 = [i for i in range(len(x)) if x[i] == u[i]]
    i2 = [i for i in range(len(x)) if x[i] == v[i]]	
    x1 = [max(u[i],x[i]-delta[i]) for i in range(len(x))]
    x2 = [min(x[i]+delta[i],v[i]) for i in range(len(x))] 
    for i in i1:
        x1[i] = x[i] + 2*delta[i]
    for i in i2:        
        x2[i] = x[i] - 2*delta[i]
    return x1,x2
