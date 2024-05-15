from typing import Union, List
import numpy as np
import sys
from typing import Tuple


class GLSUtils:
    """
    Class with util functions for MCS
    """

    def lsrange(self, xl, xu, x, p, prt, bend):
        """
        Defining line search range

        :param xl: lower bound
        :param xu: upper bound
        :param x: starting point
        :param p: Search direction
        :param prt: print command - unused in this implementation sofar
        :param bend:
        """
        if np.max(np.abs(p)) == 0:
            sys.exit('GLS Error: zero search direction in line search')

        # Find sensible step size scale
        if type(p) is not np.ndarray:
            if type(p) is not list:
                p = [p]
            p = np.asarray(p)

        if type(x) is not np.ndarray:
            if type(x) is not list:
                x = [x]
                xl = [xl]
                xu = [xu]
            x = np.asarray(x)
            xl = np.asarray(xl)
            xu = np.asarray(xu)

        # this is test for python
        if x.shape != p.shape:
            sys.exit('GLS Error: dim of x and p does not match: program is going to fail')

        pp = np.abs(p[p != 0])
        u = np.divide(np.abs(x[p != 0]), pp)
        scale = min(u)

        if scale == 0:
            u[u == 0] = np.divide(1, pp[u == 0])
            scale = min(u)

        if not bend:
            # find range of useful alp in truncated line search
            amin = -np.Inf
            amax = np.Inf
            for i in range(len(x)):
                if p[i] > 0:
                    amin = max(amin, (xl[i] - x[i]) / p[i])
                    amax = min(amax, (xu[i] - x[i]) / p[i])
                elif p[i] < 0:
                    amin = max(amin, (xu[i] - x[i]) / p[i])
                    amax = min(amax, (xl[i] - x[i]) / p[i])

            if amin > amax:
                sys.exit('GLS Error: no admissible step in line search')

        else:
            amin = np.Inf
            amax = -np.Inf
            for i in range(len(x)):
                if p[i] > 0:
                    amin = min(amin, (xl[i] - x[i]) / p[i])
                    amax = max(amax, (xu[i] - x[i]) / p[i])
                elif p[i] < 0:
                    amin = min(amin, (xu[i] - x[i]) / p[i])
                    amax = max(amax, (xl[i] - x[i]) / p[i])

        return xl, xu, x, p, amin, amax, scale

    def lssort(self, alist: List[Union[float, int]], flist: List[Union[float, int]]):
        """
        Performing the lssort

        :param alist: list of known steps
        :param flist: function values of known steps
        :return: metrics and parameters obtained from doing the lssort
        """
        perm = np.argsort(alist).tolist()
        alist.sort()
        flist = [flist[i] for i in perm if i < len(flist)]
        if len(flist) >= len(alist):
            s = len(alist)
        else:
            s = len(flist)

        up = [i < j for i, j in zip(flist[0: s - 1], flist[1: s])]
        down = [i <= j for i, j in zip(flist[1: s], flist[0: s - 1])]
        if len(down) == 1:
            down[0] = flist[s - 1] < flist[s - 2]
        else:
            down[s - 2] = flist[s - 1] < flist[s - 2]

        monotone = (sum(up) == 0 or sum(down) == 0)
        minima = [i and j for i, j in zip(up + [True], [True] + down)]
        nmin = sum(minima)

        fbest = min(flist)
        i = np.argmin(flist)

        abest = alist[i]
        fmed = np.median(flist)

        if nmin > 1:
            al = [alist[i] for i in range(len(minima)) if minima[i]]
            if abest in al:
                al.remove(abest)
            unitlen = min(np.abs(np.subtract(al, abest)))
            # TODO: investigate edge case error
        else:
            unitlen = max(abest - alist[0], alist[s - 1] - abest)

        return alist, flist, abest, fbest, fmed, up, down, monotone, minima, nmin, unitlen, s

    def lsconvex(self, alist: List[Union[float, int]], flist: List[Union[float, int]],
                 nmin: int, s: int) -> int:
        """
        Performing the lsconvex
        :param alist: list of known steps
        :param flist: function values of known steps
        :param nmin:
        :param s:
        :return: convex
        """
        if nmin > 1:
            convex = 0
        else:
            convex = 1
            for i in range(1, s - 1):
                f12 = (flist[i] - flist[i - 1]) / (alist[i] - alist[i - 1])
                f13 = (flist[i] - flist[i + 1]) / (alist[i] - alist[i + 1])
                f123 = (f13 - f12) / (alist[i + 1] - alist[i - 1])
                if f123 < 0:
                    convex = 0
                    break
            # if convex:
            #     nothing_to_do = 'done!'
        return convex

    def lssat(self, small: Union[float, int], alist: List[Union[float, int]],
              flist: List[Union[float, int]], alp: float, amin: float, amax: float, s: int,
              saturated: int) -> Tuple[float, int]:
        """
        Performing the lssat
        :param small:
        :param alist:
        :param flist:
        :param alp:
        :param amin:
        :param amin:
        :param amax:
        :param s:
        :param saturated:
        :return: alp, saturated
        """
        cont = saturated
        if cont:
            i = np.argmin(flist)
            if i == 0 or i == s - 1:
                cont = 0

        if cont:
            aa = [alist[j] for j in range(i - 1, i + 1 + 1)]
            ff = [flist[j] for j in range(i - 1, i + 1 + 1)]

            f12 = (ff[1] - ff[0]) / (aa[1] - aa[0])
            f23 = (ff[2] - ff[1]) / (aa[2] - aa[1])
            f123 = (f23 - f12) / (aa[2] - aa[0])

            if f123 > 0:
                alp = 0.5 * (aa[1] + aa[2] - f23 / f123)
                alp = max(amin, min(alp, amax))
                alptol = small * (aa[2] - aa[0])
                saturated = (abs(alist[i] - alp) <= alptol)
            else:
                saturated = 0
            # if not saturated:
            #     no_print = 0
        return alp, saturated
