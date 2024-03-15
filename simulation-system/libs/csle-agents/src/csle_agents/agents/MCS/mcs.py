# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 14:00:08 2019

@author: yl918888

Implementation of Multilevel Coordinate Search by Waltraud Huyer and Arnold Neumaier

"""
import copy
import sys

import numpy as np
from mcs_fun.basket_func import basket, basket1

# %
# MCS algorithm supporting functions =  first layer
from mcs_fun.chk_bound import check_box_bound
from mcs_fun.chk_flag import chrelerr, chvtr
from mcs_fun.chk_locks import addloc, chkloc, fbestloc
from mcs_fun.exgain import exgain
from mcs_fun.initi_func import init, initbox, subint
from mcs_fun.lsearch import lsearch
from mcs_fun.split_func import splinit, split
from mcs_fun.splrnk import splrnk
from mcs_fun.strtsw import strtsw
from mcs_fun.updtrec import updtrec
from mcs_fun.vertex_func import vertex

# %%
# ------------------------------------------------------------------------------
#                               MCS algorithm
# ------------------------------------------------------------------------------


def mcs(fcn, u, v, smax, nf, stop, iinit, local, gamma, hess, prt=1):

    # %%
    # check box bounds
    if check_box_bound(u, v):
        sys.exit("Error MCS main: out of bound")

    n = len(u)
    # initial values for the numbers of function calls (total number/local % search)
    ncall = 0
    ncloc = 0

    # create indices
    # l indicate the mid point
    l = np.multiply(1, np.ones(n)).astype(
        int
    )  # dimension n  i.e, 0 <= i < <n; for range need to add 1 each time
    # L indicate the end point or (total number of partition of the valie x in the ith dimenstion)
    # u <= x1 <= xL <= v  in the case of L == 2 (length 3) -> x0 = u (lower bound), x1 = mid point and x2 = v (upper bound)
    L = np.multiply(2, np.ones(n)).astype(
        int
    )  # dimension n  i.e, 0 <= i < <n; for range need to add 1 each time

    # definition of the initialization list
    x0 = []
    if iinit == 0:
        print
        x0.append(u)  #  lower bound point
        x0.append([(i + j) / 2 for i, j in zip(u, v)])  #  mid point
        x0.append(v)  # upper bound point
        x0 = np.array(x0).T
    elif iinit == 1:
        x0 = np.zeros((n, 3))
        for i in range(n):
            if u[i] >= 0:
                x0[i, 0] = u[i]
                x0[i, 1], x0[i, 2] = subint(u[i], v[i])
                x0[i, 1] = 0.5 * (x0[i, 0] + x0[i, 2])
            elif v[i] <= 0:
                x0[i, 2] = v[i]
                x0[i, 1], x0[i, 0] = subint(v[i], u[i])
                x0[i, 1] = 0.5 * (x0[i, 0] + x0[i, 2])
            else:
                x0[i, 1] = 0
                _, x0[i, 0], subint(0, u[i])
                _, x0[i, 2], subint(0, v[i])
    elif iinit == 2:
        x0.append([(i * 5 + j) / 6 for i, j in zip(u, v)])
        x0.append([0.5 * (i + j) for i, j in zip(u, v)])
        x0.append([(i + j * 5) / 6 for i, j in zip(u, v)])
        x0 = np.array(x0).T

    # check whether there are infinities in the initialization list
    if np.any(np.isinf(x0)):
        sys.exit("Error- MCS main: infinities in ititialization list")

    # find i*, and f0 that points to x* in the list of intial points in x0
    if iinit != 3:
        f0, istar, ncall1 = init(fcn, x0, l, L, n)
        ncall = ncall + ncall1  # increasing number of function call count

    # Computing B[x,y] in this case y = v
    # 1 base vertex
    # definition of the base vertex of the original box
    # intial x0 (mid point) is the base of vertex
    x = np.zeros(n)
    for i in range(n):
        x[i] = x0[i, l[i]]
    # 2 oposite vertex -
    # definition of the opposite vertex v1 of the original box
    # selecting one of the corener of the box
    v1 = np.zeros(n)
    for i in range(n):
        if abs(x[i] - u[i]) > abs(x[i] - v[i]):
            #  corener at the lower bound side (left of mid point)
            v1[i] = u[i]  #  go left
        else:
            # corener of the upper bound side
            v1[i] = v[i]  #  go right of mid point

    # some parameters needed for initializing large arrays
    step = 1000
    step1 = 10000
    dim = step1

    # initialization of some large arrays
    isplit = np.zeros(step1).astype(int)  # number indicating ith coardinate split
    level = np.zeros(step1).astype(int)  # number indicating level
    ipar = np.zeros(step1).astype(int)  # number
    ichild = np.zeros(step1).astype(int)  # number
    nogain = np.zeros(step1).astype(int)  # number

    f = np.zeros((2, step1))  # function value of the splitinhg float value
    z = np.zeros((2, step1))  # splitin point float value

    # initialization of the record list, the counters nboxes, nbasket, m
    # and nloc, xloc and the output flag
    record = np.zeros(smax)  #  global variable record(1:smax-1)
    nboxes = 0  #  global variable (we start with 1 box)
    nbasket = -1  #  global variable
    nbasket0 = -1
    nsweepbest = 0
    nsweep = 0  #  global variable
    m = n
    record[0] = 1  #  check 1 of Matlab = 0 of py
    nloc = 0
    xloc = []  #  global variable
    flag = 1

    # Initialize the boxes
    # use of global vaiables global: nboxes nglob xglob
    ipar, level, ichild, f, isplit, p, xbest, fbest, nboxes = initbox(
        x0, f0, l, L, istar, u, v, isplit, level, ipar, ichild, f, nboxes, prt
    )
    # generates the boxes in the initialization procedure
    f0min = fbest

    # print(stop)
    if stop[0] > 0 and stop[0] < 1:
        flag = chrelerr(fbest, stop)
    elif stop[0] == 0:
        flag = chvtr(fbest, stop[1])
    if not flag:
        print("glabal minumum as been found :", flag)
        # return  xbest,fbest,xmin,fmi,ncall,ncloc,flag
        # if the (known) minimum function value fglob has been found with the
        # required tolerance, flag is set to 0 and the program is terminated

    # the vector record is updated, and the minimal level s containing non-split boxes is computed
    s, record = strtsw(smax, level, f[0, :], nboxes, record)
    nsweep = nsweep + 1
    # sweep counter

    # Check values in MATLAB for these
    # x0, u, v, l, L, x,v1, f0, istar, f, ipar,level,ichild,f,isplit,p,xbest,fbest,nboxes,nglob,xglob, s,record,nsweep
    # %%
    xmin = []
    fmi = []
    while s < smax and ncall + 1 <= nf:
        # %%
        # print('s values',s)
        par = record[s]  # the best box at level s is the current box
        # compute the base vertex x, the opposite vertex y, the 'neighboring'
        # vertices and their function values needed for quadratic
        # interpolation and the vector n0 indicating that the ith coordinate
        # has been split n0(i) times in the history of the box
        n0, x, y, x1, x2, f1, f2 = vertex(
            par, n, u, v, v1, x0, f0, ipar, isplit, ichild, z, f, l, L
        )

        # s 'large'
        if s > 2 * n * (min(n0) + 1):
            # splitting index and splitting value z(2,par) for splitting by
            # rank are computed
            # z(2,par) is set to Inf if we split according to the init. list
            isplit[par], z[1, par] = splrnk(n, n0, p, x, y)
            splt = 1  # % indicates that the box is to be split
        else:
            # box has already been marked as not eligible for splitting by expected gain
            if nogain[par]:
                splt = 0
            else:
                # splitting by expected gain
                # compute the expected gain vector e and the potential splitting
                # index and splitting value
                e, isplit[par], z[1, par] = exgain(
                    n, n0, l, L, x, y, x1, x2, f[0, par], f0, f1, f2
                )
                fexp = f[0, par] + min(e)
                if fexp < fbest:
                    splt = 1
                else:
                    splt = 0  # the box is not split since we expect no improvement
                    nogain[par] = (
                        1  # the box is marked as not eligible for splitting by expected gain
                    )
            # end if nogain
        # end if s > 2*n*(min(n0)+1)  else
        # print(z[1,par]) # print(f[0,par])
        # %%
        if splt == 1:  # prepare for splitting
            i = isplit[par]  #  no deduction beacuse of positive index
            level[par] = 0
            # print('check len b:',len(xmin),nbasket,nbasket0)
            if z[1, par] == np.Inf:  # prepare for splitting by initialization list
                m = m + 1
                z[1, par] = m
                (
                    xbest,
                    fbest,
                    f01,
                    xmin,
                    fmi,
                    ipar,
                    level,
                    ichild,
                    f,
                    flag,
                    ncall1,
                    record,
                    nboxes,
                    nbasket,
                    nsweepbest,
                    nsweep,
                ) = splinit(
                    fcn,
                    i,
                    s,
                    smax,
                    par,
                    x0,
                    n0,
                    u,
                    v,
                    x,
                    y,
                    x1,
                    x2,
                    L,
                    l,
                    xmin,
                    fmi,
                    ipar,
                    level,
                    ichild,
                    f,
                    xbest,
                    fbest,
                    stop,
                    prt,
                    record,
                    nboxes,
                    nbasket,
                    nsweepbest,
                    nsweep,
                )
                f01 = f01.reshape(len(f01), 1)
                f0 = np.concatenate((f0, f01), axis=1)
                ncall = ncall + ncall1  #  print('call spl - 1')
            else:  # prepare for default splitting
                z[0, par] = x[i]
                (
                    xbest,
                    fbest,
                    xmin,
                    fmi,
                    ipar,
                    level,
                    ichild,
                    f,
                    flag,
                    ncall1,
                    record,
                    nboxes,
                    nbasket,
                    nsweepbest,
                    nsweep,
                ) = split(
                    fcn,
                    i,
                    s,
                    smax,
                    par,
                    n0,
                    u,
                    v,
                    x,
                    y,
                    x1,
                    x2,
                    z[:, par],
                    xmin,
                    fmi,
                    ipar,
                    level,
                    ichild,
                    f,
                    xbest,
                    fbest,
                    stop,
                    prt,
                    record,
                    nboxes,
                    nbasket,
                    nsweepbest,
                    nsweep,
                )
                ncall = ncall + ncall1  # print('call spl - 2')
            # print('check len a:',len(xmin),nbasket,nbasket0)
            if nboxes > dim:
                isplit = np.concatenate((isplit, np.zeros(step)))
                level = np.concatenate((level, np.zeros(step)))
                ipar = np.concatenate((ipar, np.zeros(step)))
                ichild = np.concatenate((ichild, np.zeros(step)))
                nogain = np.concatenate((nogain, np.zeros(step)))
                f = np.concatenate((f, np.ones((2, step))), axis=1)
                z = np.concatenate((z, np.ones((2, step))), axis=1)
                dim = nboxes + step
            if not flag:
                break
        else:  # % splt=0: no splitting, increase the level by 1
            # %%
            if s + 1 < smax:
                level[par] = s + 1
                record = updtrec(par, s + 1, f[0, :], record)  #  update record
            else:
                level[par] = 0
                nbasket = nbasket + 1
                if len(xmin) == nbasket:
                    xmin.append(copy.deepcopy(x))  # xmin[:,nbasket] = x
                    fmi.append(f[0, par])
                else:
                    xmin[nbasket] = copy.deepcopy(x)
                    fmi[nbasket] = f[0, par]
        # print('Level:',level)  #print('Record:',record)
        # %%
        # update s to split boxes
        s = s + 1
        while s < smax:
            if record[s] == 0:
                s = s + 1
            else:
                break
        # %%
        # if smax is reached, a new sweep is started
        if s == smax:
            # print(s)
            if local:
                # print(fmi, xmin,nbasket0,nbasket)
                fmiTemp = fmi[nbasket0 + 1 : nbasket + 1]
                xminTemp = xmin[nbasket0 + 1 : nbasket + 1]
                j = np.argsort(fmiTemp)
                fmiTemp = np.sort(fmiTemp)
                xminTemp = [copy.deepcopy(xminTemp[jInd]) for jInd in j]
                fmi[nbasket0 + 1 : nbasket + 1] = fmiTemp
                xmin[nbasket0 + 1 : nbasket + 1] = xminTemp
                # print('j, fmi, xmin:',j, fmi, xmin,nbasket0,nbasket, len(xmin))

                for j in range(nbasket0 + 1, nbasket + 1):
                    x = copy.deepcopy(xmin[j])
                    f1 = copy.deepcopy(fmi[j])
                    loc = chkloc(nloc, xloc, x)
                    # print('check lock:',j,x,f1,nloc, xloc,loc)
                    if loc:
                        # print('chaking basket ',nbasket0)
                        nloc, xloc = addloc(nloc, xloc, x)
                        (
                            xbest,
                            fbest,
                            xmin,
                            fmi,
                            x,
                            f1,
                            loc,
                            flag,
                            ncall1,
                            nsweep,
                            nsweepbest,
                        ) = basket(
                            fcn,
                            x,
                            f1,
                            xmin,
                            fmi,
                            xbest,
                            fbest,
                            stop,
                            nbasket0,
                            nsweep,
                            nsweepbest,
                        )
                        # print(xbest,fbest,xmin,fmi,loc,flag,ncall1)
                        ncall = ncall + ncall1
                        if not flag:
                            break
                        if loc:
                            xmin1, fmi1, nc, flag, nsweep, nsweepbest = lsearch(
                                fcn,
                                x,
                                f1,
                                f0min,
                                u,
                                v,
                                nf - ncall,
                                stop,
                                local,
                                gamma,
                                hess,
                                nsweep,
                                nsweepbest,
                            )
                            ncall = ncall + nc
                            ncloc = ncloc + nc
                            if fmi1 < fbest:
                                xbest = copy.deepcopy(xmin1)
                                fbest = copy.deepcopy(fmi1)
                                nsweepbest = nsweep
                                if not flag:
                                    nbasket0 = nbasket0 + 1
                                    nbasket = copy.deepcopy(nbasket0)
                                    if len(xmin) == nbasket:
                                        xmin.append(copy.deepcopy(xmin1))
                                        fmi.append(copy.deepcopy(fmi1))
                                    else:
                                        xmin[nbasket] = copy.deepcopy(xmin1)
                                        fmi[nbasket] = copy.deepcopy(fmi1)
                                    break

                                if stop[0] > 0 and stop[0] < 1:
                                    flag = chrelerr(fbest, stop)
                                elif stop[0] == 0:
                                    flag = chvtr(fbest, stop[1])
                                if not flag:
                                    return xbest, fbest, xmin, fmi, ncall, ncloc, flag
                                # end if
                            # end if fmi1
                            # print('chaking basket 1',nbasket0)
                            (
                                xbest,
                                fbest,
                                xmin,
                                fmi,
                                loc,
                                flag,
                                ncall1,
                                nsweep,
                                nsweepbest,
                            ) = basket1(
                                fcn,
                                np.array(xmin1),
                                fmi1,
                                xmin,
                                fmi,
                                xbest,
                                fbest,
                                stop,
                                nbasket0,
                                nsweep,
                                nsweepbest,
                            )
                            ncall = ncall + ncall1
                            # print(xbest,fbest,xmin,fmi,loc,flag,ncall1)
                            if not flag:
                                break
                            if loc:
                                # print('check1:',nbasket0, nbasket,xmin,fmi)
                                nbasket0 = nbasket0 + 1
                                if len(xmin) == nbasket0:
                                    xmin.append(copy.deepcopy(xmin1))
                                    fmi.append(copy.deepcopy(fmi1))
                                else:
                                    xmin[nbasket0] = copy.deepcopy(xmin1)
                                    fmi[nbasket0] = copy.deepcopy(fmi1)
                                # print('check2:',nbasket0, nbasket,xmin,fmi)
                                fbest, xbest = fbestloc(
                                    fmi, fbest, xmin, xbest, nbasket0, stop
                                )
                                if not flag:
                                    nbasket = nbasket0
                                    break
                # end for  basket
                nbasket = copy.deepcopy(nbasket0)
                if not flag:
                    break
            # end local
            s, record = strtsw(smax, level, f[0, :], nboxes, record)
            if prt:
                # if nsweep == 1:
                #    print(', =)
                # print('nsw   minl   nf     fbest        xbest\n')

                minlevel = s
                print("nsweep:", nsweep)
                print("minlevel:", minlevel)
                print("ncall:", ncall)
                print("fbest:", fbest)
                print("xbest: ", xbest)
                print("\n")

            if stop[0] > 1:
                if nsweep - nsweepbest >= stop[0]:
                    flag = 3
                    return xbest, fbest, xmin, fmi, ncall, ncloc, flag
            nsweep = nsweep + 1
        # end if  s ==  max
    # end while
    if ncall >= nf:
        flag = 2

    #    if local:
    #        print(len(fmi),nbasket)
    #        if len(fmi) > nbasket:
    #            for inx in range(nbasket+1,len(fmi)):
    #                del xmin[inx]
    #                del fmi[inx]
    return xbest, fbest, xmin, fmi, ncall, ncloc, flag
