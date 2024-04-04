
import numpy as np

class UtilHelpers():
    def __init__(self) -> None:
        pass


class GLSUtils(UtilHelpers):
    def __init__(self) -> None:
        super(GLSUtils, self).__init__()

    def lsrange(self, xl,xu,x,p,prt,bend):
        '''
            Defining line search range
        '''
        if np.max(np.abs(p)) == 0:
            sys.exit('GLS Error: zero search direction in line search')
        
        # find sensible step size scale
        if type(p) != np.ndarray:
            if type(p) != list:
                p = [p]
            p = np.asarray(p)
        
        if type(x) != np.ndarray:
            if type(x) != list:
                x= [x]
                xl= [xl]
                xu= [xu]
            x = np.asarray(x)
            xl = np.asarray(xl)
            xu = np.asarray(xu)

        # this is test for python
        if x.shape != p.shape:
            sys.exit('GLS Error: dim of x and p does not match: program is going to fail')
        
        pp = np.abs(p[p !=0])
        u = np.divide(np.abs(x[p != 0]),pp)
        scale = min(u)
        
        if scale == 0:
            u[u == 0] = np.divide(1,pp[u==0])
            scale = min(u) 
        
        if not bend:
            # find range of useful alp in truncated line search
            amin = -np.Inf
            amax = np.Inf
            for i in range(len(x)):
                if p[i] > 0:
                    amin = max(amin,(xl[i] - x[i])/p[i]) 
                    amax = min(amax,(xu[i] - x[i])/p[i])
                elif p[i] < 0:
                    amin = max(amin,(xu[i] - x[i])/p[i])
                    amax = min(amax,(xl[i] - x[i])/p[i])
            
            if amin > amax:
                sys.exit('GLS Error: no admissible step in line search')
                #return 
            # not needed if do not print any thing
    #        if prt:
    #            aa = amin + np.arange(101)*(amax - amin)/100
    #            ff=[]
    #            for alp in aa:
    #                xx = np.asarray([max(xl[i],min(x[i]+alp*p[i],xu[i])) for i in  range(len(x))])
    #                ff.append(feval(func,xx))
        else:
            # find range of useful alp in bent line search
            amin = np.Inf
            amax = -np.Inf
            for i in range(len(x)):
                if p[i] > 0:
                    amin = min(amin,(xl[i] - x[i])/p[i])
                    amax = max(amax,(xu[i] - x[i])/p[i])
                elif p[i] < 0:
                    amin = min(amin,(xu[i]-x[i])/p[i])
                    amax = max(amax,(xl[i]-x[i])/p[i])
    #        if prt:
    #            aa = amin +  np.arange(101)*(amax - amin)/100 
    #            ff=[]
    #            for alp in aa:
    #                xx = max(xl, min(x+alp*p,xu)) 
    #                ff.append(feval(func,xx))

        return xl,xu,x,p,amin,amax,scale#,aa,ff
                
    def lssort(self, alist,flist):
        '''
        '''
        perm = np.argsort(alist).tolist()    
        alist.sort()
        flist = [flist[i] for i in perm]
        
        s = len(alist)
        
        # find number of strict local minima, etc.
        #up = [flist[0:s-1] < flist[1:s]]
        up = [i<j for i, j in zip(flist[0:s-1], flist[1:s])]
        #down = [flist[1:s] <= flist[0:s-1]]
        down = [i<=j for i, j in zip(flist[1:s], flist[0:s-1])]
        if len(down) == 1:
            down[0] =  flist[s-1] < flist[s-2]
        else:
            down[s-2] = flist[s-1] < flist[s-2]
        
        monotone = (sum(up) == 0 or sum(down) == 0 )
        minima = [i and j for i,j in zip(up + [True], [True] + down)]
        nmin = sum(minima)
        
        fbest = min(flist)
        i = np.argmin(flist)
        
        abest = alist[i]
        fmed = np.median(flist)
        
        # distance from best minimum to next
        if nmin > 1:
            al = [alist[i] for i in range(len(minima)) if minima[i] == True]
            if abest in al:
                al.remove(abest)
            unitlen = min(np.abs(np.subtract(al,abest)))
        else:
            unitlen = max(abest - alist[0], alist[s-1] - abest)
        
        return alist, flist, abest, fbest, fmed, up, down, monotone, minima, nmin, unitlen, s

    def lsconvex(self, alist,flist,nmin,s):
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

    def lssat(self, small,alist,flist,alp,amin,amax,s,saturated):
        cont = saturated #
        
        if cont:
            # check boundary minimizer
            fmin =  min(flist)
            i =np.argmin(flist) #
            if i==0 or  i==s-1:
                cont = 0
        
        if cont:
            # select three points for parabolic interpolation
            aa = [alist[j] for j in range(i-1,i+1+1)]
            ff = [flist[j] for j in range(i-1,i+1+1)]
            
            # get divided differences 
            f12=(ff[1]-ff[0])/(aa[1]-aa[0]) #
            f23=(ff[2]-ff[1])/(aa[2]-aa[1]) #
            f123=(f23-f12)/(aa[2]-aa[0]) #
            
            if f123>0:
                # parabolic minimizer
                alp=0.5*(aa[1]+aa[2]-f23/f123) #
                alp = max(amin,min(alp,amax)) #
                alptol = small*(aa[2]-aa[0]) #
                saturated = (abs(alist[i]-alp)<=alptol)
            else:
                saturated = 0
            if not saturated:
                no_print = 0
                #print('saturation check negative')
        return alp, saturated