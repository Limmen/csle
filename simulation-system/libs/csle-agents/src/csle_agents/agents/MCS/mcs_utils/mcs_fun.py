import numpy as np
import copy
import math

class UtilHelpers():
    def __init__(self) -> None:
        pass

    def polint(self, x,f):
        '''
        quadratic polynomial interpolation
        args: 
            x(1:3)  3 pairwise distinct support points
            f(1:3)  corresponding function values
        return:
            d(1:3)  the interpolating polynomial is given by
        '''
        d = np.zeros(3)
        d[0] = f[0]
        d[1] = (f[1] - f[0])/(x[1] - x[0])
        f12 = (f[2] - f[1])/(x[2] - x[1])
        d[2] = (f12 - d[1])/(x[2] - x[0])
        return d

    def subint(self, x1, x2):
        '''
        computes [min(x,y),max(x,y)] that are neither too close nor too far away from x 
        '''
        f = 1000
        if f*abs(x1) <  1:
            if abs(x2) >  f:
                x2 = np.sign(x2)
        else:
            if abs(x2) >  f:
                x2 = 10*np.sign(x2)*abs(x1)
        x1 = x1 + (x2 -x1) / 10
        return x1, x2

    def quadpol(self, x,d,x0):
        '''
            evaluates the quadratic polynomial
        '''
        return d[0] + d[1]*(x - x0[0]) + d[2]*(x - x0[0])*(x - x0[1])

    def quadmin(self, a,b,d,x0):
        if d[2] == 0:
            if d[1] > 0:
                x = a
            else:
                x = b
        elif d[2] > 0:
            x1 = 0.5*(x0[0] + x0[1]) - 0.5*d[1]/d[2]
            if a <= x1 and x1 <= b:
                x = x1
            elif self.quadpol(a,d,x0) < self.quadpol(b,d,x0):
                x = a
            else:
                x = b
        else:
            if self.quadpol(a,d,x0) < self.quadpol(b,d,x0):
                x = a
            else:
                x = b
        return x

    def split1(self, x1,x2,f1,f2):
        if f1 <= f2:
            return x1 + 0.5*(-1 + math.sqrt(5))*(x2 - x1)
        else:
            return x1 + 0.5*(3 - math.sqrt(5))*(x2 - x1)


    def split2(self, x,y):
        '''
        % determines a value x1 for splitting the interval [min(x,y),max(x,y)]
        % is modeled on the function subint with safeguards for infinite y
        '''
        x2 = y
        if x == 0 and abs(y) > 1000:
            x2 = sign(y)
        elif x != 0 and abs(y) > 100*abs(x):
            x2 = 10*sign(y)*abs(x)
        x1 = x + 2*(x2 - x)/3
        return x1

    def vert1(self, j,z,f,x1,x2,f1,f2):
        if j == 0:
            j1 = 1 # go to right to mid mid point 
        else:
            j1 = 0# go to left end
        
        x = z[j1]
        if x1 == np.Inf:
            x1 = z[j]
            f1 = f1 + f[j]
        elif x2 == np.Inf and x1 != z[j]:
            x2 = z[j]
            f2 = f2 + f[j]
            
        return x,x1,x2,f1,f2

    def vert2(self, j,x,z,f,x1,x2,f1,f2):
        if j == 0:
            j1 = 1 # go to right mid point
        else:
            j1 = 0 # go to left endpoint

        if x1 == np.Inf:
            x1 = z[j]
            f1 = f1 + f[j]
            if x != z[j1]:
                x2 = z[j1]
                f2 = f2 + f[j1]
            #end
        elif x2 == np.Inf and x1 != z[j]:
            x2 = z[j]
            f2 = f2 + f[j]
        elif x2 == np.Inf:
            x2 = z[j1]
            f2 = f2 + f[j1]
        #end
        return x1,x2,f1,f2

    def vert3(self, j,x0,f0,L,x1,x2,f1,f2):
        if j == 0:
            k1 = 1 # go right to 1 if already at left end (right end)
            k2 = 2 # go right if already at left end (exterme right end)
        elif j == L:
            k1 = L - 2 # go left to 0 (left end)
            k2 = L - 1 # go right to 2 (right end)
        else:
            k1 = j - 1 # go left to 0 (left end)
            k2 = j + 1 # go right to 2 (right end)
        #end if
        x1 = x0[k1]
        x2 = x0[k2]
        f1 = f1 + f0[k1]
        f2 = f2 + f0[k2]
        return x1,x2,f1,f2    

    def updtf(self, n,i,x1,x2,f1,f2,fold,f):
        for i1 in range(n):
            if i1 != i:
                if x1[i1] == np.Inf:
                    f1[i1] = f1[i1] + fold - f
                if x2[i1] == np.Inf:
                    f2[i1] = f2[i1] + fold - f
        fold = f
        return f1,f2,fold


class MCSUtils(UtilHelpers):
    def __init__(self) -> None:
        super(MCSUtils, self).__init__()

    # Box bound checking
    #------------------------------------------------------------------------------
    def check_box_bound(self, u, v):
        if v < u:# upper bound < lowerbound
            print('incompatible box bounds')
            return True #  Program should stop
        elif(u==v):
            print('degenerate box bound')
            return True #  Program should stop
        else:
            return False #  Program should run

    def strtsw(self, smax, level, f, nboxes, record):
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

    def exgain(self, n, n0, l, L, x, y, x1, x2, fx, f0, f1, f2):
        '''
        % determines the splitting index, the splitting value and the expected
        % gain vector e for (potentially) splitting a box by expected gain
        % Input:
        % n        dimension of the problem
        % n0(1:n)  the ith coordinate has been split n0(i) times in the history
        %          of the box
        % l(1:n)   pointer to the initial point of the initialization list
        % L(1:n)   lengths of the initialization list
        % x(1:n)   base vertex of the box
        % y(1:n)   opposite vertex of the box
        % x1(1:n), x2(1:n), f1(1:n), f2(1:n)
        %          x1(i) and x2(i) and the corresponding function values f1(i)
        %          and f2(i) used for quadratic interpolation in the ith
        %          coordinate 
        % fx       function value at the base vertex
        % f0(1:max(L),1:n)  function values appertaining to the init. list
        % Output:
        % e(1:n)   e(i) maximal expected gain in function value by changing 
        %          coordinate i
        % isplit   splitting index
        % splval   = Inf  if n0(isplit) = 0
        %          = splitting value  otherwise
        '''
        
        e = np.zeros(n) # initialization
        emin = np.Inf;  # initialization
        for i in range(n):
            if n0[i] == 0:
                # expected gain for splitting according to the initialization list
                e[i] = min(f0[0:L[i]+1,i]) - f0[l[i],i]
                
                if e[i] < emin:
                    emin = e[i]
                    isplit = i
                    splval = np.Inf
            else:
                z1 = [x[i], x1[i], x2[i]]
                z2 = [0, f1[i] - fx, f2[i] - fx]
                d = self.polint(z1,z2)
                # safeguard against splitting too close to x(i)
                eta1, eta2 = self.subint(x[i],y[i])
                xi1 = min(eta1,eta2)
                xi2 = max(eta1,eta2)
                z = self.quadmin(xi1,xi2,d,z1)
                e[i] = self.quadpol(z,d,z1)
                if e[i] < emin:
                    emin = e[i]
                    isplit = i
                    splval = z
                    
        return e,isplit,splval

    def updtrec(self, j, s, f, record):
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

    def chkloc(self, nloc, xloc, x):
        loc = 1
        for k in range(nloc):
            if np.array_equal(x,xloc[k]):
                loc = 0
                break
        return loc

    def addloc(self, nloc, xloc, x):
        nloc = nloc + 1
        xloc.append(copy.deepcopy(x))
        return nloc, xloc

    def chrelerr(self, fbest,stop):
        fglob = stop[1]
        if fbest - fglob <= max(stop[0]*abs(fglob), stop[2]):
            flag = 0
        else:
            flag = 1
        
        return flag

    def chvtr(self, f,vtr):
        if f <= vtr:
            flag = 0
        else:
            flag = 1
            
        return flag

    def fbestloc(self, fmi,fbest,xmin,xbest,nbasket0,stop):
        if fmi[nbasket0] < fbest:
            fbest = copy.deepcopy(fmi[nbasket0])
            xbest = copy.deepcopy(xmin[nbasket0])
            #flag = chrelerr(fbest,stop)
        return fbest, xbest#, flag

    def splrnk(self, n,n0,p,x,y):
        '''
            Determines the splitting index and splitting value for splitting a box by rank
            :param n: dimension of the problem
            :param p: ranking of estimated variability of the function in the different coordinates
            :param x: base vertex of the box
            :param y: opposite vertex of the box
            :return : splitting index
            isplit   splitting index
        '''

        isplit = 0
        n1 = n0[0]
        p1 = p[0]
        for i in range(1,n):
            if n0[i] < n1 or (n0[i] == n1 and p[i] < p1):
                isplit = i
                n1 = n0[i]
                p1 = p[i]
        if n1 > 0:
            splval = self.split2(x[isplit],y[isplit])
        else:
            splval =  np.Inf
        return isplit,splval

    def genbox(self, par,level0,nchild,f0):
        ipar = par #  set parent box index
        level = level0 #  set level value of the box
        ichild = nchild #  set number of child
        f = f0 # set optimal value of the box
        return ipar,level,ichild,f

    def vertex(self, j,n,u,v,v1,x0,f0,ipar,isplit,ichild,z,f,l,L):
        '''
            # initialization
            # The coordinates of x, y, x1 and x2 are initially set to Inf to 
            # indicate that these quantities haven't been found yet in the course of
            # pursuing the history of box j
        '''
        x = np.multiply(np.Inf,np.ones(n))
        y = np.multiply(np.Inf,np.ones(n))
        x1 = np.multiply(np.Inf,np.ones(n))
        x2 = np.multiply(np.Inf,np.ones(n))
        f1 = np.zeros(n)
        f2 = np.zeros(n)
        # counting tthe number of time boxes has been split in ith direction
        n0 = np.zeros(n)
        fold = f[0,j]
        m = j
        
        while m > 0:
            if isplit[ipar[m]] < 0:
                i = int(abs(isplit[ipar[m]])) -1 #  negative 1 for making index fit to array in python
            else:
                i = int(abs(isplit[ipar[m]])) #  no negative 
                
            n0[i] = n0[i] + 1 # increase the counting tthe number of time boxes has been split in ith direction
            
            # ichild holds value from level 1 and not from level 0 there > 0 is ok
            if ichild[m] == 1:
                if x[i] == np.Inf or x[i] == z[0,ipar[m]]:
                    x[i], x1[i], x2[i], f1[i], f2[i] = self.vert1(1,z[:,ipar[m]], f[:,ipar[m]], x1[i], x2[i], f1[i], f2[i])
                else:
                    f1,f2,fold = self.updtf(n,i,x1,x2,f1,f2,fold,f[0,ipar[m]])
                    x1[i],x2[i],f1[i],f2[i] = self.vert2(0,x[i],z[:,ipar[m]],f[:,ipar[m]],x1[i],x2[i],f1[i],f2[i])
            elif ichild[m] >= 2:
                f1,f2,fold = self.updtf(n,i,x1,x2,f1,f2,fold,f[0,ipar[m]])
                if x[i] == np.Inf or x[i] == z[1, ipar[m]]:
                    x[i],x1[i],x2[i],f1[i],f2[i] = self.vert1(0,z[:,ipar[m]],f[:,ipar[m]],x1[i],x2[i],f1[i],f2[i])
                else:
                    x1[i],x2[i],f1[i],f2[i] = self.vert2(1,x[i],z[:,ipar[m]],f[:,ipar[m]],x1[i],x2[i],f1[i],f2[i])
            
            # ichild holds value from level 1 and not from level 0 there > 0 is ok
            if 1 <= ichild[m] and ichild[m] <= 2 and y[i] == np.Inf:
                y[i] = self.split1(z[0,ipar[m]],z[1,ipar[m]],f[0,ipar[m]],f[1,ipar[m]])
            
            # ichild holds value from level 1 and not from level 0 there > 0 is ok
            if ichild[m] < 0:
                # box m was generated by splitting according to the init. list
                # x0[i,j1] = ith coordinate of the base vertex of box m
                # the ith coordinate of the opposite vertex is the golden section 
                # split of x0[i,j2] and x0[i,j2+1] for 1 <= j2 <= L[i] - 1, it is 
                # u[i] for j1 = 1 and v[i] for j2 = L[i] 
                # x0[i,j1+j3] = ith coordinate of the 'neighboring vertex'
                if u[i] < x0[i,0]:
                    j1 = math.ceil(abs(ichild[m])/2)  
                    j2 = math.floor(abs(ichild[m])/2)
                    if (abs(ichild[m])/2 < j1 and j1 > 0) or j1 == L[i]+1:
                        j3 = -1
                    else:
                        j3 = 1
                else:
                    j1 = math.floor(abs(ichild[m])/2) + 1
                    j2 = math.ceil(abs(ichild[m])/2)
                    if abs(ichild[m])/2 + 1 > j1 and j1 < L[i]+1:
                        j3 = 1
                    else:
                        j3 = -1
                #reduce index by 1 to fit to the dimenstion length for o to n-1
                j1 -=1
                j2 -=1
            
                if int(isplit[ipar[m]]) < 0: # box m was generated in the init. procedure
                    k = copy.deepcopy(i)
                else:
                    # box m was generated by a later split according to the init.
                    # list; k points to the corresponding function values  
                    k = int(z[0,ipar[m]])
                
                if j1 != l[i] or (x[i] != np.Inf and x[i] != x0[i,l[i]]):
                    f1,f2,fold = self.updtf(n,i,x1,x2,f1,f2,fold,f0[l[i],k])
                    
                if x[i] == np.Inf or x[i] == x0[i,j1]:
                    x[i] = x0[i,j1]
                    if x1[i] == np.Inf:
                        x1[i],x2[i],f1[i],f2[i] = self.vert3(j1,x0[i,:],f0[:,k],L[i],x1[i],x2[i],f1[i],f2[i])
                    elif x2[i] == np.Inf and x1[i] != x0[i,j1+j3]:
                        x2[i] = x0[i,j1+j3]
                        f2[i] = f2[i] + f0[j1+j3,k]
                    elif x2[i] == np.Inf:
                        if j1 != 1 and j1 != L[i]:
                            x2[i] = x0[i,j1-j3]
                            f2[i] = f2[i] + f0[j1-j3,k]
                        else:
                            x2[i] = x0[i,j1+2*j3]
                            f2[i] = f2[i] + f0[j1+2*j3,k]
                        #end j1 != 1
                    #end x1[i] == np.Inf
                else:
                    if x1[i] == np.Inf:
                        x1[i] = x0[i,j1]
                        f1[i] = f1[i] + f0[j1,k]
                        if x[i] != x0[i,j1+j3]:
                            x2[i] = x0[i,j1+j3];
                            f2[i] = f2[i] + f0[j1+j3,k]
                        # end  if x[i] != x0[i,j1+j3]
                    elif x2[i] == np.Inf:
                        if x1[i] != x0[i,j1]:
                            x2[i] = x0[i,j1]
                            f2[i] = f2[i] + f0[j1,k]
                        elif x[i] != x0[i,j1+j3]:
                            x2[i] = x0[i,j1+j3]
                            f2[i] = f2[i] + f0[j1+j3,k]
                        else:
                            if j1 != 1 and j1 != L[i]:
                                x2[i] = x0[i,j1-j3]
                                f2[i] = f2[i] + f0[j1-j3,k]
                            else:
                                x2[i] = x0[i,j1+2*j3]
                                f2[i] = f2[i] + f0[j1+2*j3,k]
                            # end j1 != 1 and j1 != L[i]
                        # end x1[i] != x0[i,j1]
                    #end x1[i] == np.Inf
                #end  x[i] == np.Inf or x[i] == x0[i,j1]
                if y[i] == np.Inf:
                    if j2 == -1: #  make it nagative since in python index case it can become nagative
                        y[i] = u[i]
                    elif j2 == L[i]:
                        y[i] = v[i]
                    else:
                        y[i] = self.split1(x0[i,j2],x0[i,j2+1],f0[j2,k],f0[j2+1,k])
                    #end
                #end if yi
            # end if ichild[m] < 0
            m = ipar[m]
        # end while
        for i in range(n):
            if x[i] == np.Inf:
                x[i] = x0[i,l[i]]
                x1[i],x2[i],f1[i],f2[i] = self.vert3(l[i],x0[i,:],f0[:,i],L[i],x1[i],x2[i],f1[i],f2[i])
            
            if y[i] == np.Inf:
                y[i] = v1[i]

        return n0,x,y,x1,x2,f1,f2

    def initbox(self, theta0,f0,l,L,istar,u,v,isplit,level,ipar,ichild,f,nboxes,prt):
        """
        Generates the boxes in the initializaiton procedure
        """
        n = len(u)
        # intilize the ith histopy with the folowing:
        # parent  box index, 
        # level of parent box, 
        # split index of the parent box, 
        # number of child
        # 
        
        # parent of the ith box 
        # it is the index into the number of boxex 
        ipar[0]= -1 #  parent box is index -1 for the root box
        # history level o the parent box: initilize to 1 as the 0 < level s < smax of root box is 1
        # indicate box 0 with level value s = 1
        level[0] = 1
        # ichild indicate the child of box 0 
        ichild[0] = 1
        # optimi value of the box is theta0
        f[0,0] = f0[l[0],0]
        # intilize partent box  = 0
        par = 0 # index of the parent box (biously 0 in this case as box index start with z)
        
        
        var = np.zeros(n)
        for i in range(n):
            #print('parent box',par)
            # boxes split in the init. procedure get a negative splitting index of the ith coordinate (dimension)
            isplit[par] = -i-1 # set a negative index value
            nchild = 0
            # check if x left endpoint is > lower bound (left endpoint)
            # if so - genetrate a box
            if theta0[i,0] >  u[i]:
                nboxes = nboxes + 1 # one extra box is generated for the parent box
                nchild = nchild + 1 # therefore incerase number of child by 1 of the parent box
                # set parent of this ith box split in the ithe direction (dimension)
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = MCSUtils().genbox(par, level[par]+1,-nchild, f0[0, i])
            # end if
            
            if L[i] == 2:
                v1 = v[i]
            else:
                v1 = theta0[i,2]
            # end if
            
            # pollynomial interpolation to get three points for
            d = self.polint(theta0[i,0:3],f0[0:3,i])
            xl = self.quadmin(u[i],v1,d,theta0[i,0:3])
            fl = self.quadpol(xl,d,theta0[i,0:3])
            xu = self.quadmin(u[i],v1,-d,theta0[i,0:3])
            fu = self.quadpol(xu,d,theta0[i,0:3])
            
            if istar[i] == 0:
                if xl < theta0[i,0]:
                    par1 = nboxes  # label of the current box for the next coordinate 
                else:
                    par1 = nboxes + 1
            #end istart
        
            for j in range(L[i]):
                nboxes = nboxes + 1
                nchild = nchild + 1
                if f0[j,i] <= f0[j+1,i]:
                    s = 1
                else:
                    s = 2
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = MCSUtils().genbox(par,level[par]+s,-nchild,f0[j,i])
                #if prt: splval = split1(theta0[i,j],theta0[i,j+1],f0[j,i],f0[j+1,i])
                
                if j >= 1:
                    if istar[i] == j:
                        if xl <= theta0[i,j]:
                            par1 = nboxes - 1  # label of the current box for the next coordinate 
                        else:
                            par1 = nboxes
                    #end istar
                    if j <= L[i] - 2:
                        d = polint(theta0[i,j:j+1],f0[j:j+1,i])
                        if j < L[i] - 2:
                            u1 = theta0[i,j+1]
                        else:
                            u1 = v[i] 
                        # end if
                        xl = quadmin(theta0[i,j],u1,d,theta0[i,j:j+1])
                        fl = min(quadpol(xl,d,theta0[i,j:j+1]),fl)
                        xu = quadmin(theta0[i,j],u1,-d,theta0[i,j:j+1])
                        fu = max(quadpol(xu,d,theta0[i,j:j+1]),fu)
                    #end j < Li -2
                # end if j > = 1
                nboxes = nboxes + 1
                nchild = nchild + 1
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = MCSUtils().genbox(par,level[par]+3-s,-nchild,f0[j+1,i])
            #end for j
            if theta0[i,L[i]] < v[i]:
                nboxes = nboxes + 1
                nchild = nchild + 1            
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0,nboxes] = MCSUtils().genbox(par,level[par]+1,-nchild,f0[L[i],i])
                
            if istar[i] == L[i]:
                if theta0[i,L[i]] < v[i]:
                    if xl <= theta0[i,L[i]]:
                        par1 = nboxes - 1  # label of the current box for the next coordinate 
                    else:
                        par1 = nboxes
                    #end if xl < theta0
                else:
                    par1 = nboxes
                #end if theta0 < v
            #end if istart
            var[i] = fu - fl
            
            # the quadratic model is taken as a crude measure of the variability in the ith component
            level[par] = 0  # box is marked as split
            par = par1
        #end for
        fbest = f0[istar[n-1],n-1] #best function value after the init. procedure
        p = np.zeros(n).astype(int)
        xbest = np.zeros(n)
        #print(nboxes)
        for i in range(n):
            #var0 = max(var) 
            p[i] = np.argmax(var)
            var[p[i]] = -1
            xbest[i] = theta0[i,istar[i]]  # best point after the init. procedured
        
        return  ipar,level,ichild,f,isplit,p,xbest,fbest,nboxes

    def neighbor(self, x, delta, u, v):
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
