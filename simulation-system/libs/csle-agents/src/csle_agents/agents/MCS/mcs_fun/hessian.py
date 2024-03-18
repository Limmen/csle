#------------------------------------------------------------------------------
def hessian(i,k,x,x0,f,f0,g,G):
    '''
    computes the element G(i,k) of the Hessian of the local quadratic model
    '''
    #print(i,x[i],x0[i],f,f,g[i],G[i,i])
    #print(k,x[k],x0[k],f,f,g[k],G[k,k]) 
    h = f-f0 -g[i]*(x[i]-x0[i])  -g[k]*(x[k]-x0[k])  -0.5*G[i,i]*(pow((x[i]-x0[i]),2))  -0.5*G[k,k]*pow((x[k]-x0[k]),2)
    h = h / (x[i]- x0[i])/(x[k]-x0[k])
    return h