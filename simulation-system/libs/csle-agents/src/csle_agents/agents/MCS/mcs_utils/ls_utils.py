import numpy as np
from numpy.typing import NDArray
from typing import Any
import sys
from scipy.sparse import spdiags
from scipy import sparse


class Minq():
    def __init__(self) -> None:
        pass

    def ldlrk1(self, L, d, alp, u):
        p = np.array([])
        if alp == 0:
            return L, d, p

        eps = 2.2204e-16
        n = u.shape[0]
        neps = n * eps

        L0 = L
        d0 = d

        # update
        for k in [i for i in range(n) if u[i] != 0]:
            delta = d[k] + alp * pow(u[k], 2)
            if alp < 0 and delta <= neps:
                p = np.zeros(n)
                p[k] = 1
                p0Krange = [i for i in range(0, k + 1)]
                p0K = np.asarray([p[i] for i in p0Krange])
                L0K = np.asarray([[L[i, j] for j in p0Krange] for i in p0Krange])
                p0K = np.linalg.solve(L0K, p0K)
                p = np.asarray([p0K[i] if (i in p0Krange) else p[i] for i in range(len(p))])
                L = L0
                d = d0
                return L, d, p

            q = d[k] / delta
            d[k] = delta
            ind = [i for i in range(k + 1, n)]
            LindK = np.asarray([L[i, k] for i in ind])
            uk = u[k]
            c = np.dot(LindK, uk)
            for i in range(len(ind)):
                L[ind[i], k] = LindK[i] * q + (alp * u[k] / delta) * u[ind[i]]

            for i in range(len(ind)):
                u[ind[i]] = u[ind[i]] - c[i]

            alp = alp * q
            if alp == 0:
                break
        return L, d, p


class UtilHelpers():
    def __init__(self) -> None:
        pass

    def ldldown(self, L, d, j):
        n = d.shape[0]
        if j < n:
            I = [i for i in range(0, j)]
            K = [i for i in range(j + 1, n)]

            LKK = np.asarray([[L[i, j] for j in K] for i in K])
            dK = np.asarray([d[i] for i in K])
            LKj = np.asarray([L[i, j] for i in K])
            LKK, dK, _ = Minq().ldlrk1(LKK, dK, d[j], LKj)
            d[K] = dK
            r1 = L[I, :]
            r2 = sparse.coo_matrix((1, n)).toarray()
            if len(I) == 0:
                r3 = np.concatenate((sparse.coo_matrix((n - j - 1, 1)).toarray(), LKK), axis=1)
                L = np.concatenate((r2, r3), axis=0)
            else:
                LKI = np.asarray([[L[i, j] for j in I] for i in K])
                if len(K) != 0:
                    r3 = np.concatenate((LKI, sparse.coo_matrix((n - j - 1, 1)).toarray(), LKK), axis=1)
                    L = np.concatenate((r1, r2, r3), axis=0)
                else:
                    L = np.concatenate((r1, r2), axis=0)
            L[j, j] = 1
        else:
            L[n - 1, 0: n - 1] = sparse.coo_matrix((1, n - 1)).toarray()
        d[j] = 1
        return L, d

    def ldlup(self, L, d, j, g, eps):
        p = np.array([])
        # eps = 2.2204e-16
        n = d.shape[0]
        I = [i for i in range(0, j)]
        K = [i for i in range(j + 1, n)]

        if j == 0:
            v = np.zeros(0)
            delta = g[j]
            if delta <= n * eps:
                p = np.asarray([1] + np.zeros(n - 1).tolist())
                return L, d, p
            w = np.asarray([g[i] / delta for i in K])
            L[j, I] = v.T
            d[j] = delta
            # p = np.asarray(p)
            return L, d, p
        LII = np.asarray([[L[i, j] for j in I] for i in I])
        gI = [g[i] for i in I]
        u = np.linalg.solve(LII, gI)
        dI = [d[i] for i in I]
        v = np.divide(u, dI)
        delta = g[j] - np.dot(u.T, v)
        if delta <= n * eps:
            p = np.asarray(np.linalg.solve(LII.T, v).tolist() + [-1] + np.zeros(n - j - 1).tolist())
            return L, d, p

        if len(K) != 0:
            LKI = np.asarray([[L[i, j] for j in I] for i in K])
            gK = np.asarray([g[i] for i in K])
            w = np.divide(np.subtract(gK, np.dot(LKI, u)), delta)
            LKK = np.asarray([[L[i, j] for j in K] for i in K])
            dK = np.asarray([d[i] for i in K])
            LKK, dK, q = Minq().ldlrk1(LKK, dK, -delta, w)
            d[K] = dK
        else:
            q = []

        if len(q) == 0:
            r1 = L[I, :]
            r2 = np.asarray(v.T.tolist() + [1] + L[j, K].tolist())
            r2 = r2.reshape((1, len(r2)))
            if len(K) != 0:
                r3 = np.concatenate((LKI, w.reshape(len(w), 1), LKK), axis=1)

                L = np.concatenate((r1, r2, r3), axis=0)
            else:
                L = np.concatenate((r1, r2), axis=0)
            d[j] = delta
        else:
            r1 = L[0: j + 1, :]
            r2 = np.concatenate((LKI, L[K, j].reshape(len(L[K, j]), 1), LKK), axis=1)
            L = np.concatenate((r1, r2), axis=0)
            w = w.reshape((len(w), 1))
            q.reshape((len(q)), 1)
            pi = np.dot(w.T, q)
            piv = np.multiply(pi, v)
            LKIq = np.dot(LKI.T, q)
            pivLKIq = np.subtract(piv.flatten(), LKIq.flatten())
            piSolve = np.linalg.solve(LII.T, pivLKIq)
            p = np.asarray(piSolve.flatten().tolist() + (-1 * pi).flatten().tolist() + q.tolist())
        return L, d, p

    def getalp(self, alpu, alpo, gTp, pTGp):
        '''
            Gives minimizer alp in [alpu,alpo] for a univariate quadratic q(alp)=alp*gTp+0.5*alp^2*pTGp
        '''
        lba = False
        uba = False

        ier = 0
        if alpu == -np.Inf and (pTGp < 0 or (pTGp == 0 and gTp > 0)):
            ier = 1
            lba = True
        if alpo == np.Inf and (pTGp < 0 or (pTGp == 0 and gTp < 0)):
            ier = 1
            uba = True
        if ier:
            alp = np.NAN
            return alp, lba, uba, ier

        if pTGp == 0 and gTp == 0:
            alp = 0
        elif pTGp <= 0:
            if alpu == -np.Inf:
                lba = False
            elif alpo == np.Inf:
                lba = True
            else:
                lba = (2 * gTp + (alpu + alpo) * pTGp > 0)
            uba = not lba
        else:
            alp = -gTp / pTGp
            lba = (alp <= alpu)
            uba = (alp >= alpo)

        if lba:
            alp = alpu
        if uba:
            alp = alpo

        if abs(alp) == np.Inf:
            gTp, pTGp, alpu, alpo, alp, lba, uba, ier
        return alp, lba, uba, ier

    def minqsub(self, nsub, free, L, dd, K, G, n, g, x, xo, xu, convex,
                xx, fct, nfree, unfix, alp, alpu, alpo, lba, uba, ier, subdone, eps):
        nsub = nsub + 1
        # eps = 2.2204e-16

        freelK = [i for i in range(len(free)) if (free < K)[i] is True]
        for j in freelK:
            L, dd = self.ldldown(L, dd, j)
            K[j] = False

        definite = 1
        freeuK = [i for i in range(len(free)) if (free > K)[i] is True]
        for j in freeuK:
            p = np.zeros(n)
            if n > 1:
                p = np.asarray([G[i, j] if K[i] is True else p[i] for i in range(len(K))])
            p[j] = G[j, j]
            L, dd, p = self.ldlup(L, dd, j, p, eps)
            definite = (len(p) == 0)
            if not definite:
                break
            K[j] = True

        if definite:
            p = np.zeros(n)
            p = np.asarray([g[i] if K[i] is True else p[i] for i in range(len(K))])
            LPsolve = np.linalg.solve(L, p)
            LPsolve = np.divide(LPsolve, dd)
            p = np.multiply(-1, np.linalg.solve(L.T, LPsolve))

        p = (x + p) - x
        ind = [i for i in range(len(p)) if p[i] != 0]
        if len(ind) == 0:
            unfix = 1
            subdone = 0
            return (nsub, free, L, dd, K, G, n, g, x, xo, xu, convex, xx, fct,
                    nfree, alp, alpu, alpo, lba, uba, ier, unfix, subdone)
        pp = np.asarray([p[i] for i in ind])
        oo = np.subtract([xo[i] for i in ind], [x[i] for i in ind]) / pp
        uu = np.subtract([xu[i] for i in ind], [x[i] for i in ind]) / pp
        alpu = max([oo[i] for i in range(len(ind)) if pp[i] < 0] + [uu[i] for i in range(
            len(ind)) if pp[i] > 0] + [-np.inf])
        alpo = min([oo[i] for i in range(len(ind)) if pp[i] > 0] + [uu[i] for i in range(
            len(ind)) if pp[i] < 0] + [np.inf])
        if alpo <= 0 or alpu >= 0:
            sys.exit('programming error: no alp')

        gTp = np.dot(g.T, p)
        agTp = np.dot(np.abs(g).T, np.abs(p))
        if abs(gTp) < 100 * eps * agTp:
            gTp = 0
        pTGp = np.dot(p.T, np.dot(G, p))
        if convex:
            pTGp = max(0, pTGp)
        if not definite and pTGp > 0:
            pTGp = 0

        alp, lba, uba, ier = self.getalp(alpu, alpo, gTp, pTGp)
        if ier:
            x = np.zeros(n)
            if lba:
                x = -p
            else:
                x = p
            return (nsub, free, L, dd, K, G, n, g, x, xo, xu, convex, xx,
                    fct, nfree, alp, alpu, alpo, lba, uba, ier, unfix, subdone)

        unfix = not (lba or uba)
        for k in range(0, len(ind)):
            ik = ind[k]
            if alp == uu[k]:
                xx[ik] = xu[ik]
                free[ik] = 0
            elif alp == oo[k]:
                xx[ik] = xo[ik]
                free[ik] = 0
            else:
                xx[ik] = xx[ik] + alp * p[ik]
            if abs(xx[ik]) == np.Inf:
                ik, alp, p[ik]
                sys.exit('infinite xx in minq')

        nfree = sum(free)
        subdone = 1
        return (nsub, free, L, dd, K, G, n, g, x, xo, xu, convex, xx,
                fct, nfree, alp, alpu, alpo, lba, uba, ier, unfix, subdone)


class LSUtils(UtilHelpers):
    def __init__(self) -> None:
        super(LSUtils, self).__init__()

    def lsguard(self, alp, alist, amax, amin, small):
        asort = alist
        asort.sort()
        s = len(asort)

        al = asort[0] - (asort[s - 1] - asort[0]) / small
        au = asort[s - 1] + (asort[s - 1] - asort[0]) / small
        alp = max(al, min(alp, au))
        alp = max(amin, min(alp, amax))

        if abs(alp - asort[0]) < small * (asort[1] - asort[0]):
            alp = (2 * asort[0] + asort[1]) / 3

        if abs(alp - asort[s - 1]) < small * (asort[s - 1] - asort[s - 1 - 1]):
            alp = (2 * asort[s - 1] + asort[s - 1 - 1]) / 3

        return alp

    def lssplit(self, i, alist, flist, short):
        if flist[i] < flist[i + 1]:
            fac = short
        elif flist[i] > flist[i + 1]:
            fac = 1 - short
        else:
            fac = 0.5

        alp = alist[i] + fac * (alist[i + 1] - alist[i])
        return alp, fac

    def minq(self, gam, c, G, xu, xo, prt, eps):
        '''
        Minimizes an affine quadratic form subject to simple bounds.
        Using coordinate searches and reduced subspace minimizations, using LDL^T factorization updates
        fct  =  gam + c^T x + 0.5 x^T G x s.t. x in [xu,xo] (xu <= xo is assumed),
        where G is a symmetric n x n matrix, not necessarily definite
        (if G is indefinite, only a local minimum is found)
        if G is sparse, it is assumed that the ordering is such that
        a sparse modified Cholesky factorization is feasible

        :param prt:	printlevel
        :param xx:	initial guess (optional)
        :param x: minimizer (but unbounded direction if ier = 1)
        :param fct:	optimal function value
        :param ier:	0  (local minimizer found)
        '''

        convex = 0
        n = G.shape[0]

        ier = 0
        if G.shape[1] != n:
            ier = -1
            print('minq: Hessian has wrong dimension')
            x = np.NAN + np.zeros(n)
            fct = np.NAN
            nsub = -1
            return x, fct, ier

        if c.shape[0] != n:
            ier = -1
            print('minq: linear term has wrong dimension')
        if xu.shape[0] != n:
            ier = -1
            print('minq: lower bound has wrong dimension')

        if xo.shape[0] != n:
            ier = -1
            print('minq: lower bound has wrong dimension')

        if 'xx' in locals():
            xx: NDArray[Any] = locals()["xx"]
            if xx.shape[0] != n:
                ier = -1
                print('minq: lower bound has wrong dimension')
        else:
            xx = np.zeros(n)
   
        if ier == -1:
            x = np.NAN + np.zeros(n)
            fct = np.NAN
            nsub = -1
            return x, fct, ier

        maxit = 3 * n

        nitrefmax = 3
        xx = np.asarray([max(xu[i], min(xx[i], xo[i])) for i in range(len(xx))])

        # eps = 2.2204e-16
        hpeps = 100 * eps
        G = G + spdiags(hpeps * np.diag(G), 0, n, n).toarray()

        K = np.zeros(n, dtype=bool)
        L = np.eye(n)
        dd = np.ones(n)

        free = np.zeros(n, dtype=bool)
        nfree = 0
        nfree_old = -1

        fct = np.Inf
        nsub = 0
        unfix = 1
        nitref = 0
        improvement = 1
 
        while 1:
            if np.linalg.norm(xx, np.inf) == np.inf:
                sys.exit('infinite xx in minq.m')

            g = np.dot(G, xx) + c
            fctnew = gam + np.dot(0.5 * xx.T, (c + g))
            if not improvement:
                ier = 0
                break
            elif nitref > nitrefmax:

                ier = 0
                break
            elif nitref > 0 and nfree_old == nfree and fctnew >= fct:
                ier = 0
                break
            elif nitref == 0:
                x = xx
                fct = min(fct, fctnew)
            else:
                x = xx
                fct = fctnew
            if nitref == 0 and nsub >= maxit:
                ier = 99
                break
            count = 0
            k = -1
            while 1:
                while count <= n:
                    count = count + 1
                    if k == n - 1:
                        k = -1
                    k = k + 1
                    if free[k] or unfix:
                        break
                if count > n:

                    break
                q = G[:, k]
                alpu = xu[k] - x[k]
                alpo = xo[k] - x[k]

                alp, lba, uba, ier = self.getalp(alpu, alpo, g[k], q[k])

                if ier:
                    x = np.zeros(n)
                    if lba:
                        x[k] = -1
                    else:
                        x[k] = 1

                    return x, fct, ier

                xnew = x[k] + alp
                if prt and nitref > 0:
                    xnew, alp

                if lba or xnew <= xu[k]:
                    if alpu != 0:
                        x[k] = xu[k]
                        g = g + alpu * q
                        count = 0
                    free[k] = 0
                elif uba or xnew >= xo[k]:
                    if alpo != 0:
                        x[k] = xo[k]
                        g = g + alpo * q
                        count = 0
                    free[k] = 0
                else:
                    if alp != 0.0:
                        if prt > 1 and not free[k]:
                            unfixstep = [x[k], alp]
                        x[k] = xnew
                        g = g + alp * q
                        free[k] = 1

            nfree = sum(free)
            if (unfix and nfree_old == nfree):
                g = np.dot(G, x) + c
                nitref = nitref + 1
            else:
                nitref = 0
            nfree_old = nfree
            gain_cs = fct - gam - np.dot(0.5 * x.T, (c + g))
            improvement = (gain_cs > 0 or not unfix)
            xx = x
            if not improvement or nitref > nitrefmax:

                nothing_to_do = 'done!'
            elif nitref > nitrefmax:
                nothing_to_do = 'done!'
            elif nfree == 0:
                unfix = 1
            else:
                subdone = 0
                (nsub, free, L, dd, K, G, n, g, x, xo, xu, convex, xx, fct,
                 nfree, alp, alpu, alpo, lba, uba, ier, unfix, subdone) = self.minqsub(nsub, free, L, dd, K, G, n, g, x,
                                                                                       xo, xu, convex, xx, fct, nfree,
                                                                                       unfix, alp, alpu, alpo, lba, uba,
                                                                                       ier, subdone, eps)
                if not subdone:
                    return x, fct, ier
                if ier:
                    return x, fct, ier
        return x, fct, ier

    def quartic(self, a, x):
        return (((a[0] * x + a[1]) * x + a[2]) * x + a[3]) * x + a[4]
