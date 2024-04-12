import numpy as np
import copy
import math
import sys


class UtilHelpers():
    def __init__(self) -> None:
        pass

    def polint(self, x, f):
        '''
        Quadratic polynomial interpolation
        
        :param x:  3 pairwise distinct support points
        :param f: corresponding function values
        return d: the interpolating polynomial is given by
        '''
        d = np.zeros(3)
        d[0] = f[0]
        d[1] = (f[1] - f[0]) / (x[1] - x[0])
        f12 = (f[2] - f[1]) / (x[2] - x[1])
        d[2] = (f12 - d[1]) / (x[2] - x[0])
        return d

    def subint(self, x1, x2):
        '''
        computes [min(x,y),max(x,y)] that are neither too close nor too far away from x
        '''
        f = 1000
        if f * abs(x1) < 1:
            if abs(x2) > f:
                x2 = np.sign(x2)
        else:
            if abs(x2) > f:
                x2 = 10 * np.sign(x2) * abs(x1)
        x1 = x1 + (x2 - x1) / 10
        return x1, x2

    def quadpol(self, x, d, x0):
        '''
            Evaluates the quadratic polynomial
        '''
        return d[0] + d[1] * (x - x0[0]) + d[2] * (x - x0[0]) * (x - x0[1])

    def quadmin(self, a, b, d, x0):
        if d[2] == 0:
            if d[1] > 0:
                x = a
            else:
                x = b
        elif d[2] > 0:
            x1 = 0.5 * (x0[0] + x0[1]) - 0.5 * d[1] / d[2]
            if a <= x1 and x1 <= b:
                x = x1
            elif self.quadpol(a, d, x0) < self.quadpol(b, d, x0):
                x = a
            else:
                x = b
        else:
            if self.quadpol(a, d, x0) < self.quadpol(b, d, x0):
                x = a
            else:
                x = b
        return x

    def split1(self, x1, x2, f1, f2):
        if f1 <= f2:
            return x1 + 0.5 * (-1 + math.sqrt(5)) * (x2 - x1)
        else:
            return x1 + 0.5 * (3 - math.sqrt(5)) * (x2 - x1)

    def split2(self, x, y):
        '''
        determines a value x1 for splitting the interval [min(x,y),max(x,y)]
        is modeled on the function subint with safeguards for infinite y
        '''
        x2 = y
        if x == 0 and abs(y) > 1000:
            x2 = np.sign(y)
        elif x != 0 and abs(y) > 100 * abs(x):
            x2 = 10 * np.sign(y) * abs(x)
        x1 = x + 2 * (x2 - x) / 3
        return x1

    def vert1(self, j, z, f, x1, x2, f1, f2):
        if j == 0:
            j1 = 1
        else:
            j1 = 0
        x = z[j1]
        if x1 == np.Inf:
            x1 = z[j]
            f1 = f1 + f[j]
        elif x2 == np.Inf and x1 != z[j]:
            x2 = z[j]
            f2 = f2 + f[j]
            
        return x, x1, x2, f1, f2

    def vert2(self, j, x, z, f, x1, x2, f1, f2):
        if j == 0:
            j1 = 1
        else:
            j1 = 0

        if x1 == np.Inf:
            x1 = z[j]
            f1 = f1 + f[j]
            if x != z[j1]:
                x2 = z[j1]
                f2 = f2 + f[j1]
        elif x2 == np.Inf and x1 != z[j]:
            x2 = z[j]
            f2 = f2 + f[j]
        elif x2 == np.Inf:
            x2 = z[j1]
            f2 = f2 + f[j1]

        return x1, x2, f1, f2

    def vert3(self, j, x0, f0, L, x1, x2, f1, f2):
        if j == 0:
            k1 = 1
            k2 = 2
        elif j == L:
            k1 = L - 2
            k2 = L - 1
        else:
            k1 = j - 1
            k2 = j + 1
        x1 = x0[k1]
        x2 = x0[k2]
        f1 = f1 + f0[k1]
        f2 = f2 + f0[k2]
        return x1, x2, f1, f2

    def updtf(self, n, i, x1, x2, f1, f2, fold, f):
        for i1 in range(n):
            if i1 != i:
                if x1[i1] == np.Inf:
                    f1[i1] = f1[i1] + fold - f
                if x2[i1] == np.Inf:
                    f2[i1] = f2[i1] + fold - f
        fold = f
        return f1, f2, fold


class MCSUtils(UtilHelpers):
    def __init__(self) -> None:
        super(MCSUtils, self).__init__()

    def check_box_bound(self, u, v):
        if v < u:
            print('incompatible box bounds')
            return True
        elif (u == v):
            print('degenerate box bound')
            return True
        else:
            return False

    def strtsw(self, smax, level, f, nboxes, record):

        record = np.zeros(smax).astype(int)
        s = smax
        for j in range(nboxes + 1):
            if level[j] > 0:
                if level[j] < s:
                    s = level[j]
                if not record[level[j]]:
                    record[level[j]] = j

                elif f[j] < f[record[level[j]]]:
                    record[level[j]] = j
        return s, record

    def exgain(self, n, n0, l, L, x, y, x1, x2, fx, f0, f1, f2):
        '''
        Determines the splitting index, the splitting value and the expected
        gain vector e for (potentially) splitting a box by expected gain
        :param n: dimension of the problem
        :param n0: the ith coordinate has been split n0(i) times in the history of the box
        :param l: pointer to the initial point of the initialization list
        :param L: lengths of the initialization list
        :param x: base vertex of the box
        :param y: opposite vertex of the box
        :param x1: corresponding parameter/coordinate value
        :param x2: corresponding parameter/coordinate value
        :param f1: corresponding function value
        :param f2: corresponding function value
        :param fx: function value at the base vertex
        :param f0:  function values appertaining to the init. list
        :return e: maximal expected gain in function value by changing coordinate i
        :return isplit: splitting index
        :return splval: Inf  if n0(isplit) = 0, splitting value  otherwise
        '''
        
        e = np.zeros(n)
        emin = np.Inf
        for i in range(n):
            if n0[i] == 0:
                e[i] = min(f0[0: L[i] + 1, i]) - f0[l[i], i]
                if e[i] < emin:
                    emin = e[i]
                    isplit = i
                    splval = np.Inf
            else:
                z1 = [x[i], x1[i], x2[i]]
                z2 = [0, f1[i] - fx, f2[i] - fx]
                d = self.polint(z1, z2)
                eta1, eta2 = self.subint(x[i], y[i])
                xi1 = min(eta1, eta2)
                xi2 = max(eta1, eta2)
                z = self.quadmin(xi1, xi2, d, z1)
                e[i] = self.quadpol(z, d, z1)
                if e[i] < emin:
                    emin = e[i]
                    isplit = i
                    splval = z
        return e, isplit, splval

    def updtrec(self, j, s, f, record):
        '''
            :param j: label of a box
            :param s: its level
            :param f: vector containing the base vertex function values of the already defined boxes.
            Updates the pointer record(s) to the best non-split box at level s
            :param record: record list
        '''
        if len(record) < s:
            record[s] = j
        elif record[s] == 0:
            record[s] = j
        elif f[j] < f[record[s]]:
            record[s] = j

        return record

    def chkloc(self, nloc, xloc, x):
        loc = 1
        for k in range(nloc):
            if np.array_equal(x, xloc[k]):
                loc = 0
                break
        return loc

    def addloc(self, nloc, xloc, x):
        nloc = nloc + 1
        xloc.append(copy.deepcopy(x))
        return nloc, xloc

    def chrelerr(self, fbest, stop):
        fglob = stop[1]
        if fbest - fglob <= max(stop[0] * abs(fglob), stop[2]):
            flag = 0
        else:
            flag = 1

        return flag

    def chvtr(self, f, vtr):
        if f <= vtr:
            flag = 0
        else:
            flag = 1

        return flag

    def fbestloc(self, fmi, fbest, xmin, xbest, nbasket0, stop):
        if fmi[nbasket0] < fbest:
            fbest = copy.deepcopy(fmi[nbasket0])
            xbest = copy.deepcopy(xmin[nbasket0])
        return fbest, xbest

    def splrnk(self, n, n0, p, x, y):
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
        for i in range(1, n):
            if n0[i] < n1 or (n0[i] == n1 and p[i] < p1):
                isplit = i
                n1 = n0[i]
                p1 = p[i]
        if n1 > 0:
            splval = self.split2(x[isplit], y[isplit])
        else:
            splval = np.Inf
        return isplit, splval

    def genbox(self, par, level0, nchild, f0):
        ipar = par
        level = level0
        ichild = nchild
        f = f0
        return ipar, level, ichild, f

    def vertex(self, j, n, u, v, v1, x0,
               f0, ipar, isplit, ichild, z, f, l, L):
        x = np.multiply(np.Inf, np.ones(n))
        y = np.multiply(np.Inf, np.ones(n))
        x1 = np.multiply(np.Inf, np.ones(n))
        x2 = np.multiply(np.Inf, np.ones(n))
        f1 = np.zeros(n)
        f2 = np.zeros(n)

        n0 = np.zeros(n)
        fold = f[0, j]
        m = j

        while m > 0:
            if isplit[ipar[m]] < 0:
                i = int(abs(isplit[ipar[m]])) - 1
            else:
                i = int(abs(isplit[ipar[m]]))

            n0[i] = n0[i] + 1

            if ichild[m] == 1:
                if x[i] == np.Inf or x[i] == z[0, ipar[m]]:
                    x[i], x1[i], x2[i], f1[i], f2[i] = self.vert1(1, z[:, ipar[m]],
                                                                  f[:, ipar[m]], x1[i], x2[i], f1[i], f2[i])
                else:
                    f1, f2, fold = self.updtf(n, i, x1, x2, f1, f2, fold, f[0, ipar[m]])
                    x1[i], x2[i], f1[i], f2[i] = self.vert2(0, x[i], z[:, ipar[m]],
                                                            f[:, ipar[m]], x1[i], x2[i], f1[i], f2[i])
            elif ichild[m] >= 2:
                f1, f2, fold = self.updtf(n, i, x1, x2, f1, f2, fold, f[0, ipar[m]])
                if x[i] == np.Inf or x[i] == z[1, ipar[m]]:
                    x[i], x1[i], x2[i], f1[i], f2[i] = self.vert1(0, z[:, ipar[m]],
                                                                  f[:, ipar[m]], x1[i], x2[i], f1[i], f2[i])
                else:
                    x1[i], x2[i], f1[i], f2[i] = self.vert2(1, x[i], z[:, ipar[m]],
                                                            f[:, ipar[m]], x1[i], x2[i], f1[i], f2[i])

            if 1 <= ichild[m] and ichild[m] <= 2 and y[i] == np.Inf:
                y[i] = self.split1(z[0, ipar[m]], z[1, ipar[m]], f[0, ipar[m]], f[1, ipar[m]])

            if ichild[m] < 0:
                if u[i] < x0[i, 0]:
                    j1 = math.ceil(abs(ichild[m]) / 2)
                    j2 = math.floor(abs(ichild[m]) / 2)
                    if (abs(ichild[m]) / 2 < j1 and j1 > 0) or j1 == L[i] + 1:
                        j3 = -1
                    else:
                        j3 = 1
                else:
                    j1 = math.floor(abs(ichild[m]) / 2) + 1
                    j2 = math.ceil(abs(ichild[m]) / 2)
                    if abs(ichild[m]) / 2 + 1 > j1 and j1 < L[i] + 1:
                        j3 = 1
                    else:
                        j3 = -1
                j1 -= 1
                j2 -= 1
            
                if int(isplit[ipar[m]]) < 0:
                    k = copy.deepcopy(i)
                else:
                    k = int(z[0, ipar[m]])

                if j1 != l[i] or (x[i] != np.Inf and x[i] != x0[i, l[i]]):
                    f1, f2, fold = self.updtf(n, i, x1, x2, f1, f2, fold, f0[l[i], k])
                if x[i] == np.Inf or x[i] == x0[i, j1]:
                    x[i] = x0[i, j1]
                    if x1[i] == np.Inf:
                        x1[i], x2[i], f1[i], f2[i] = self.vert3(j1, x0[i, :], f0[:, k], L[i], x1[i], x2[i], f1[i],
                                                                f2[i])
                    elif x2[i] == np.Inf and x1[i] != x0[i, j1 + j3]:
                        x2[i] = x0[i, j1 + j3]
                        f2[i] = f2[i] + f0[j1 + j3, k]
                    elif x2[i] == np.Inf:
                        if j1 != 1 and j1 != L[i]:
                            x2[i] = x0[i, j1 - j3]
                            f2[i] = f2[i] + f0[j1 - j3, k]
                        else:
                            x2[i] = x0[i, j1 + 2 * j3]
                            f2[i] = f2[i] + f0[j1 + 2 * j3, k]
                else:
                    if x1[i] == np.Inf:
                        x1[i] = x0[i, j1]
                        f1[i] = f1[i] + f0[j1, k]
                        if x[i] != x0[i, j1 + j3]:
                            x2[i] = x0[i, j1 + j3]
                            f2[i] = f2[i] + f0[j1 + j3, k]
                    elif x2[i] == np.Inf:
                        if x1[i] != x0[i, j1]:
                            x2[i] = x0[i, j1]
                            f2[i] = f2[i] + f0[j1, k]
                        elif x[i] != x0[i, j1 + j3]:
                            x2[i] = x0[i, j1 + j3]
                            f2[i] = f2[i] + f0[j1 + j3, k]
                        else:
                            if j1 != 1 and j1 != L[i]:
                                x2[i] = x0[i, j1 - j3]
                                f2[i] = f2[i] + f0[j1 - j3, k]
                            else:
                                x2[i] = x0[i, j1 + 2 * j3]
                                f2[i] = f2[i] + f0[j1 + 2 * j3, k]
                if y[i] == np.Inf:
                    if j2 == -1:
                        y[i] = u[i]
                    elif j2 == L[i]:
                        y[i] = v[i]
                    else:
                        y[i] = self.split1(x0[i, j2], x0[i, j2 + 1], f0[j2, k], f0[j2 + 1, k])
            m = ipar[m]
        for i in range(n):
            if x[i] == np.Inf:
                x[i] = x0[i, l[i]]
                x1[i], x2[i], f1[i], f2[i] = self.vert3(l[i], x0[i, :], f0[:, i], L[i], x1[i], x2[i], f1[i], f2[i])
            if y[i] == np.Inf:
                y[i] = v1[i]

        return n0, x, y, x1, x2, f1, f2

    def initbox(self, theta0, f0, l, L, istar, u, v,
                isplit, level, ipar, ichild, f, nboxes, prt):
        """
        Generates the boxes in the initializaiton procedure
        """
        n = len(u)
 
        ipar[0] = -1
        level[0] = 1
        ichild[0] = 1

        f[0, 0] = f0[l[0], 0]

        par = 0

        var = np.zeros(n)
        for i in range(n):
            isplit[par] = - i - 1
            nchild = 0
            if theta0[i, 0] > u[i]:
                nboxes = nboxes + 1
                nchild = nchild + 1
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0, nboxes] =\
                    MCSUtils().genbox(par, level[par] + 1, - nchild, f0[0, i])
            if L[i] == 2:
                v1 = v[i]
            else:
                v1 = theta0[i, 2]
            d = self.polint(theta0[i, 0: 3], f0[0: 3, i])
            xl = self.quadmin(u[i], v1, d, theta0[i, 0: 3])
            fl = self.quadpol(xl, d, theta0[i, 0: 3])
            xu = self.quadmin(u[i], v1, - d, theta0[i, 0: 3])
            fu = self.quadpol(xu, d, theta0[i, 0: 3])

            if istar[i] == 0:
                if xl < theta0[i, 0]:
                    par1 = nboxes
                else:
                    par1 = nboxes + 1

            for j in range(L[i]):
                nboxes = nboxes + 1
                nchild = nchild + 1
                if f0[j, i] <= f0[j + 1, i]:
                    s = 1
                else:
                    s = 2
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0, nboxes] =\
                    MCSUtils().genbox(par, level[par] + s, - nchild, f0[j, i])

                if j >= 1:
                    if istar[i] == j:
                        if xl <= theta0[i, j]:
                            par1 = nboxes - 1
                        else:
                            par1 = nboxes
                    if j <= L[i] - 2:
                        d = self.polint(theta0[i, j: j + 1], f0[j: j + 1, i])
                        if j < L[i] - 2:
                            u1 = theta0[i, j + 1]
                        else:
                            u1 = v[i]
                        xl = self.quadmin(theta0[i, j], u1, d, theta0[i, j: j + 1])
                        fl = min(self.quadpol(xl, d, theta0[i, j: j + 1]), fl)
                        xu = self.quadmin(theta0[i, j], u1, -d, theta0[i, j: j + 1])
                        fu = max(self.quadpol(xu, d, theta0[i, j: j + 1]), fu)

                nboxes = nboxes + 1
                nchild = nchild + 1
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0, nboxes] =\
                    MCSUtils().genbox(par, level[par] + 3 - s, -nchild, f0[j + 1, i])
            if theta0[i, L[i]] < v[i]:
                nboxes = nboxes + 1
                nchild = nchild + 1
                ipar[nboxes], level[nboxes], ichild[nboxes], f[0, nboxes] = \
                    MCSUtils().genbox(par, level[par] + 1, -nchild, f0[L[i], i])

            if istar[i] == L[i]:
                if theta0[i, L[i]] < v[i]:
                    if xl <= theta0[i, L[i]]:
                        par1 = nboxes - 1
                    else:
                        par1 = nboxes
                else:
                    par1 = nboxes
            var[i] = fu - fl
            
            level[par] = 0
            par = par1
        fbest = f0[istar[n - 1], n - 1]
        p = np.zeros(n).astype(int)
        xbest = np.zeros(n)
        for i in range(n):
            p[i] = np.argmax(var)
            var[p[i]] = -1
            xbest[i] = theta0[i, istar[i]]
        return ipar, level, ichild, f, isplit, p, xbest, fbest, nboxes

    def neighbor(self, x, delta, u, v):
        '''
            computes 'neighbors' x1 and x2 of x needed for making triple search
            and building a local quadratic model such that x(i), x1(i), x2(i) are
            pairwise distinct for i = 1,...,n
        '''
        i1 = [i for i in range(len(x)) if x[i] == u[i]]
        i2 = [i for i in range(len(x)) if x[i] == v[i]]
        x1 = [max(u[i], x[i] - delta[i]) for i in range(len(x))]
        x2 = [min(x[i] + delta[i], v[i]) for i in range(len(x))]
        for i in i1:
            x1[i] = x[i] + 2 * delta[i]
        for i in i2:
            x2[i] = x[i] - 2 * delta[i]
        return x1, x2

    def polint1(self, x, f):
        '''
            quadratic polynomial interpolation
        '''
        f13 = (f[2] - f[0]) / (x[2] - x[0])
        f12 = (f[1] - f[0]) / (x[1] - x[0])
        f23 = (f[2] - f[1]) / (x[2] - x[1])
        g = f13 + f12 - f23
        G = 2 * (f13 - f12) / (x[2] - x[1])
        return g, G

    def hessian(self, i, k, x, x0, f, f0, g, G):
        '''
        computes the element G(i,k) of the Hessian of the local quadratic model
        '''
        h = f - f0 - g[i] * (x[i] - x0[i]) - g[k] * (x[k] - x0[k]) - 0.5 * G[i, i] * (pow((x[i] - x0[i]), 2))\
            - 0.5 * G[k, k] * pow((x[k] - x0[k]), 2)
        h = h / (x[i] - x0[i]) / (x[k] - x0[k])
        return h

    def get_theta0(self, iinit, u, v, n):
        theta0 = []
        if iinit == 0:
            theta0.append(u)
            theta0.append([(i + j) / 2 for i, j in zip(u, v)])
            theta0.append(v)
            theta0 = np.array(theta0).T
        elif iinit == 1:
            theta0 = np.zeros((n, 3))
            for i in range(n):
                if u[i] >= 0:
                    theta0[i, 0] = u[i]
                    theta0[i, 1], theta0[i, 2] = self.subint(u[i], v[i])
                    theta0[i, 1] = 0.5 * (theta0[i, 0] + theta0[i, 2])
                elif v[i] <= 0:
                    theta0[i, 2] = v[i]
                    theta0[i, 1], theta0[i, 0] = self.subint(v[i], u[i])
                    theta0[i, 1] = 0.5 * (theta0[i, 0] + theta0[i, 2])
                else:
                    theta0[i, 1] = 0
                    _, theta0[i, 0], self.subint(0, u[i])
                    _, theta0[i, 2], self.subint(0, v[i])
        elif iinit == 2:
            theta0.append([(i * 5 + j) / 6 for i, j in zip(u, v)])
            theta0.append([0.5 * (i + j) for i, j in zip(u, v)])
            theta0.append([(i + j * 5) / 6 for i, j in zip(u, v)])
            theta0 = np.array(theta0).T

        if np.any(np.isinf(theta0)):
            sys.exit("Error- MCS main: infinities in ititialization list")
        return theta0
