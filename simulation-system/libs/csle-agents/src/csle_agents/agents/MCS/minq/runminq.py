#test minq.m, minqdef.m, minqsep.m

%reset -f
%clear
#%%
import numpy as np
from optimization.parameter.mcs.minq.minq_data import minq_data
from optimization.parameter.mcs.minq.minqsep import minqsep
from optimization.parameter.mcs.minq.minqdef import minqdef


n=7 # 
m=10 # 
p=0.8 # 		#approx. fraction of activities and equalities
newdata = 0

if newdata:
    #create random data satisfying the KKT conditions
    A = np.random.rand(m,n) 
    c = np.random.rand(n) # 
    d = np.random.rand(n) # 
    ydes = np.random.rand(m)-p # 
    act = ydes>p
    ydes = np.asarray([0*ydes[i] if act[i] else ydes[i] for i in range(ydes.shape[0])])
    #ydes.resize(m,1)
    eq =  np.asarray([i<0 for i in ydes])
    #eq.resize(m,1)
    xdes = (np.dot(A.T,ydes)-c)/d
    res = np.random.rand(m)
    res = np.asarray([0*res[i] if not act[i] else res[i] for i in range(res.shape[0])])
    #res.resize(m,1)
    b = np.dot(A,xdes)-res
    prt=0
else:
    A,act,b,c,d,eq,m,n,p,res,xdes,ydes = minq_data()
    prt=0
#%%
for cas in [1,2]:
    if cas==1:
        print('test of minqsep.m')
        x,y,ier = minqsep(c,d,A,b,eq,prt)
    else:
        print('test of minqdef.m')
        x,y,ier = minqdef(c,np.diag(d),A,b,eq,prt)
        
        #printing
#        compldes = [ydes, A*xdes-b] # 
#        compl = [y,A*x-b] # 
#        act_eq = [act,eq]'
#        ydif = [ydes,y]
#        print('usually two equal columns') # 
#        print('but sometimes the dual is not unique')
#        #xdif=[xdes,x]
#        print('xdif should have two equal columns')
#        #ier
#        if cas==2:
#            break
#        
#        cont = input('enter return (next test) or 0 (quit)>') 
#        if isempty(cont):
#            continue
#        elif cont==0:
#            break

