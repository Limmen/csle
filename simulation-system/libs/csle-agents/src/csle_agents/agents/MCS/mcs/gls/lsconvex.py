# lsconvex 
# check convexity
def lsconvex(alist,flist,nmin,s):
    if nmin > 1: 
        convex=0  
    else:
        convex=1    
        for i in range(1,s-1):
            f12 = (flist[i]-flist[i-1])/(alist[i]-alist[i-1])
            f13 = (flist[i]-flist[i+1])/(alist[i]-alist[i+1])
            f123 = (f13-f12)/(alist[i+1]-alist[i-1])
            if f123<0:
                #print('not convex')
                convex=0 
                break  
        if convex:
            nothing_to_do = 'done!'
            #print('convex')
    return convex
