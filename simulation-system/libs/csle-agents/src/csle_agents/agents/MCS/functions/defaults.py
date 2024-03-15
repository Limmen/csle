# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 07:43:31 2019

@author: yl918888
"""
import sys


def defaults(name):
    """
    retun defualty values of the functions
    args:
        name: function names
    return functon default values
    """
    if name == "myfun":
        return myfun()
    if name == "gpr":
        return gpr()
    elif name == "bra":
        return bra()
    elif name == "cam":
        return cam()
    elif name == "sh5":
        return sh5()
    elif name == "sh7":
        return sh7()
    elif name == "s10":
        return s10()
    elif name == "hm3":
        return hm3()
    elif name == "hm6":
        return hm6()
    else:
        sys.exit("Default: no function available with this name")


def myfun():
    """
    TODO: implemment your funciton [functions.py]')
    TODO: implemment your funciton papramter [defualts.py]')
    """
    ## For domain [-1, 1] u and v will be
    u = [-20, -20, -20]
    v = [20, 20, 20]

    nglob = 1  # number of gloabl optmial to be searhed
    fglob = 0.0  # known  gloabl optmia value
    xglob = [0, 0, 0]  # # known  gloabl optmia vector if any

    return u, v, nglob, fglob, xglob


def gpr():
    """
    # Goldstein-Price function
    """
    u = [-2, -2]
    v = [2, 2]
    nglob = 1
    fglob = 3
    xglob = [0, -1.0]
    return u, v, nglob, fglob, xglob


def bra():
    """
    # Branin's function
    """
    u = [-5, 0]
    v = [10, 15]
    nglob = 3
    fglob = 0.397887357729739
    xglob = [
        [9.42477796, 2.47499998],
        [-3.14159265, 12.27500000],
        [3.14159265, 2.27500000],
    ]
    return u, v, nglob, fglob, xglob


def cam():
    """
    # six camel hump
    """
    u = [-3, -2]  # lower bound
    v = [3, 2]  # upper bound
    nglob = 2
    fglob = -1.0316284535
    xglob = [[0.08984201, -0.71265640], [0.71265640, -0.08984201]]
    return u, v, nglob, fglob, xglob


def sh5():
    """
    # Shekel 5
    """
    u = [0, 0, 0, 0]
    v = [10, 10, 10, 10]
    fglob = -10.1531996790582
    xglob = [4, 4, 4, 4]
    nglob = 1
    return u, v, nglob, fglob, xglob


def sh7():
    """
    # Shekel 7
    """
    u = [0, 0, 0, 0]
    v = [10, 10, 10, 10]
    fglob = -10.4029405668187
    xglob = [4, 4, 4, 4]
    nglob = 1
    return u, v, nglob, fglob, xglob


def s10():
    """
    # Shekel 10
    """
    u = [0, 0, 0, 0]
    v = [10, 10, 10, 10]
    fglob = -10.5364098166920
    xglob = [4, 4, 4, 4]
    nglob = 1
    return u, v, nglob, fglob, xglob


def hm3():
    """
    # Hartman 3
    """
    u = [0, 0, 0]
    v = [1, 1, 1]
    fglob = -3.86278214782076
    xglob = [0.1, 0.55592003, 0.85218259]
    nglob = 1
    return u, v, nglob, fglob, xglob


def hm6():
    """
    # Hartman 6
    """
    u = [0, 0, 0, 0, 0, 0]
    v = [1, 1, 1, 1, 1, 1]
    fglob = -3.32236801141551
    xglob = [0.20168952, 0.15001069, 0.47687398, 0.27533243, 0.31165162, 0.65730054]
    nglob = 1
    return u, v, nglob, fglob, xglob
