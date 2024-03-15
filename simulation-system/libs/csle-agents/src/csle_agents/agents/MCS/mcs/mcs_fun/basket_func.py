import copy

import numpy as np
from functions.functions import feval
from mcs_fun.chk_flag import chrelerr, chvtr

# ------------------------------------------------------------------------------
from mcs_fun.initi_func import init


# ------------------------------------------------------------------------------
def basket(fcn, x, f, xmin, fmi, xbest, fbest, stop, nbasket, nsweep, nsweepbest):
    """ """
    loc = 1
    flag = 1
    ncall = 0
    if not nbasket:
        return xbest, fbest, xmin, fmi, x, f, loc, flag, ncall, nsweep, nsweepbest

    dist = np.zeros(nbasket + 1)
    for k in range(len(dist)):
        dist[k] = np.linalg.norm(np.subtract(x, xmin[k]))

    dist1 = np.sort(dist)
    ind = np.argsort(dist)

    for k in range(nbasket + 1):
        i = ind[k]
        if fmi[i] <= f:
            print("här då")
            print(xmin[i])
            print(x)
            p = xmin[i] - x
            y1 = x + 1 / 3 * p
            f1 = feval(fcn, y1)
            ncall = ncall + 1
            if f1 <= f:
                y2 = x + 2 / 3 * p
                f2 = feval(fcn, y2)
                ncall = ncall + 1
                if f2 > max(f1, fmi[i]):
                    if f1 < f:
                        x = y1
                        f = f1
                        if f < fbest:
                            fbest = f
                            xbest = copy.deepcopy(x)
                            nsweepbest = nsweep
                            if stop[0] > 0 and stop[0] < 1:
                                flag = chrelerr(fbest, stop)
                            elif stop[0] == 0:
                                flag = chvtr(fbest, stop[1])
                            if not flag:
                                return (
                                    xbest,
                                    fbest,
                                    xmin,
                                    fmi,
                                    x,
                                    f,
                                    loc,
                                    flag,
                                    ncall,
                                    nsweep,
                                    nsweepbest,
                                )
                else:
                    if f1 < min(f2, fmi[i]):
                        f = f1
                        x = copy.deepcopy(y1)
                        if f < fbest:
                            fbest = f
                            xbest = copy.deepcopy(x)
                            nsweepbest = nsweep
                            if stop[0] > 0 and stop[0] < 1:
                                flag = chrelerr(fbest, stop)
                            elif stop[0] == 0:
                                flag = chvtr(fbest, stop[1])
                            if not flag:
                                return (
                                    xbest,
                                    fbest,
                                    xmin,
                                    fmi,
                                    x,
                                    f,
                                    loc,
                                    flag,
                                    ncall,
                                    nsweep,
                                    nsweepbest,
                                )
                        elif f2 < min(f1, fmi[i]):
                            f = f2
                            x = copy.deepcopy(y2)
                            if f < fbest:
                                fbest = f
                                xbest = copy.deepcopy(x)
                                nsweepbest = nsweep
                                if stop[0] > 0 and stop[0] < 1:
                                    flag = chrelerr(fbest, stop)
                                elif stop[0] == 0:
                                    flag = chvtr(fbest, stop[1])
                                if not flag:
                                    return (
                                        xbest,
                                        fbest,
                                        xmin,
                                        fmi,
                                        x,
                                        f,
                                        loc,
                                        flag,
                                        ncall,
                                        nsweep,
                                        nsweepbest,
                                    )
                        else:
                            loc = 0
                            break

    return xbest, fbest, xmin, fmi, x, f, loc, flag, ncall, nsweep, nsweepbest


# ------------------------------------------------------------------------------
def basket1(fcn, x, f, xmin, fmi, xbest, fbest, stop, nbasket, nsweep, nsweepbest):
    """ """
    loc = 1
    flag = 1
    ncall = 0
    if not nbasket:
        return xbest, fbest, xmin, fmi, loc, flag, ncall, nsweep, nsweepbest

    dist = np.zeros(nbasket + 1)
    for k in range(len(dist)):
        dist[k] = np.linalg.norm(np.subtract(x, xmin[k]))

    dist1 = np.sort(dist)
    ind = np.argsort(dist)

    for k in range(nbasket + 1):
        i = ind[k]
        print("wah")
        print(x)
        print("hej")
        print(xmin[i])
        p = xmin[i] - x
        y1 = x + 1 / 3 * p
        f1 = feval(fcn, y1)
        ncall = ncall + 1
        if f1 <= max(fmi[i], f):
            y2 = x + 2 / 3 * p
            f2 = feval(fcn, y2)
            ncall = ncall + 1
            if f2 <= max(f1, fmi[i]):
                if f < min(min(f1, f2), fmi[i]):
                    fmi[i] = f
                    xmin[i] = copy.deepcopy(x)
                    if fmi[i] < fbest:
                        fbest = copy.deepcopy(fmi[i])
                        xbest = copy.deepcopy(xmin[i])
                        nsweepbest = nsweep
                        if stop[0] > 0 and stop[0] < 1:
                            flag = chrelerr(fbest, stop)
                        elif stop[0] == 0:
                            flag = chvtr(fbest, stop[1])
                        if not flag:
                            return (
                                xbest,
                                fbest,
                                xmin,
                                fmi,
                                loc,
                                flag,
                                ncall,
                                nsweep,
                                nsweepbest,
                            )
                    # end fmi[i] < fbest:
                    loc = 0
                    break
                elif f1 < min(min(f, f2), fmi[i]):
                    fmi[i] = f1
                    xmin[i] = copy.deepcopy(y1)
                    if fmi[i] < fbest:
                        fbest = copy.deepcopy(fmi[i])
                        xbest = copy.deepcopy(xmin[i])
                        nsweepbest = copy.deepcopy(nsweep)

                        if stop[0] > 0 and stop[0] < 1:
                            flag = chrelerr(fbest, stop)
                        elif stop[0] == 0:
                            flag = chvtr(fbest, stop[1])
                        if not flag:
                            return (
                                xbest,
                                fbest,
                                xmin,
                                fmi,
                                loc,
                                flag,
                                ncall,
                                nsweep,
                                nsweepbest,
                            )
                    # end fmi[i] < fbest: elif
                    loc = 0
                    break
                elif f2 < min(min(f, f1), fmi[i]):
                    fmi[i] = f2
                    xmin[i] = copy.deepcopy(y2)
                    if fmi[i] < fbest:
                        fbest = copy.deepcopy(fmi[i])
                        xbest = copy.deepcopy(xmin[i])
                        nsweepbest = nsweep
                        if stop[0] > 0 and stop[0] < 1:
                            flag = chrelerr(fbest, stop)
                        elif stop[0] == 0:
                            flag = chvtr(fbest, stop[1])
                        if not flag:
                            return (
                                xbest,
                                fbest,
                                xmin,
                                fmi,
                                loc,
                                flag,
                                ncall,
                                nsweep,
                                nsweepbest,
                            )
                    # end elseif
                    loc = 0
                    break
                else:
                    loc = 0
                    break
    return xbest, fbest, xmin, fmi, loc, flag, ncall, nsweep, nsweepbest
