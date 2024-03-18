# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 07:08:08 2019

@author: yl918888
"""
import math
import sys

import numpy as np


def feval(fcn, x):
    """
    Function definations
    """
    if fcn == "myfun":
        return myfun(x)
    if fcn == "glstest":
        return glstest(x)
    elif fcn == "bra":
        return bra(x)
    elif fcn == "cam":
        return cam(x)
    elif fcn == "gpr":
        return gpr(x)
    elif fcn == "sh5":
        return sh5(x)
    elif fcn == "sh7":
        return sh7(x)
    elif fcn == "s10":
        return s10(x)
    elif fcn == "hm3":
        return hm3(x)
    elif fcn == "hm6":
        return hm6(x)
    else:
        print("no funciton with such name implemented")


# ------------------------------------------------------------------------------------------
def myfun(x):
    # print('TODO implemment your funciton [functions.py]')

    return (x[0] - 0.2) ** 2 + (x[1] - 0.01) ** 2 + (x[2] - 2.4) ** 2


# ------------------------------------------------------------------------------------------
def glstest(x):
    cas = 3
    if cas == 1:
        f = ((3 * x - 1) * x - 2) * x - 1
    elif cas == 2:
        f = pow((3 * x - 1), 3)
    elif cas == 3:
        f = pow((3 * x - 1), 2)
    elif cas == 4:
        f = (x + 1) * math.sin(10 * x + 1)
    return np.asscalar(f)


# ------------------------------------------------------------------------------------------
def bra(x):
    """
    Branin's function
    """
    a = 1
    b = 5.1 / (4 * math.pi * math.pi)
    c = 5 / math.pi
    d = 6
    h = 10
    ff = 1 / (8 * math.pi)
    if len(x) != 2:
        print("bar function takes only a vector length 2")
        sys.exit()

    x1 = x[0]
    x2 = x[1]
    f = a * pow((x2 - b * pow(x1, 2) + c * x1 - d), 2) + h * (1 - ff) * math.cos(x1) + h
    return f


def cam(x):
    """
    six-hump camel function - dimension n = 2
    arg:
        x =  vector do dimention 2
    """
    # print('cam was called')
    # x is the vector of length 2
    if len(x) != 2:
        print("cam function takes only a vector length 2")
        sys.exit()

    x1 = x[0]
    x2 = x[1]
    f = (
        (4 - 2.1 * pow(x1, 2) + pow(x1, 4) / 3) * pow(x1, 2)
        + x1 * x2
        + (-4 + 4 * pow(x2, 2)) * pow(x2, 2)
    )
    return f


def gpr(x):
    """
    # Goldstein-Price function
    """
    if len(x) != 2:
        print("Goldstein function takes only a vector length 2")
        sys.exit()

    x1 = x[0]
    x2 = x[1]
    f = (
        1
        + pow((x1 + x2 + 1), 2)
        * (19 - 14 * x1 + 3 * pow(x1, 2) - 14 * x2 + 6 * x1 * x2 + 3 * pow(x2, 2))
    ) * (
        30
        + pow((2 * x1 - 3 * x2), 2)
        * (18 - 32 * x1 + 12 * pow(x1, 2) + 48 * x2 - 36 * x1 * x2 + 27 * pow(x2, 2))
    )
    return f


def sh5(x):
    """
    # Shekel5 function
    """
    if len(x) != 4:
        print("Shekel5 function takes only a vector length 4")
        sys.exit()

    a = np.asarray(
        [
            [4.0, 1.0, 8.0, 6.0, 3.0],
            [4.0, 1.0, 8.0, 6.0, 7.0],
            [4.0, 1.0, 8.0, 6.0, 3.0],
            [4.0, 1.0, 8.0, 6.0, 7.0],
        ]
    )

    c = np.asarray([0.1, 0.2, 0.2, 0.4, 0.4])

    d = np.zeros(5)
    for i in range(5):
        b = (x - a[:, i]) ** 2
        d[i] = sum(b)
    f = -sum((c + d) ** (-1))
    return f


def sh7(x):
    """
    # Shekel7 function
    """
    if len(x) != 4:
        print("Shekel7 function takes only a vector length 4")
        sys.exit()

    a = np.asarray(
        [
            [4, 1, 8, 6, 3, 2, 5],
            [4, 1, 8, 6, 7, 9, 5],
            [4, 1, 8, 6, 3, 2, 3],
            [4, 1, 8, 6, 7, 9, 3],
        ]
    )

    c = np.asarray([0.1, 0.2, 0.2, 0.4, 0.4, 0.6, 0.3])

    d = np.zeros(7)
    for i in range(7):
        b = (x - a[:, i]) ** 2
        d[i] = sum(b)
    f = -sum((c + d) ** (-1))
    return f


def s10(x):
    """
    # Shekel10 function
    """
    if len(x) != 4:
        print("Shekel10 function takes only a vector length 4")
        sys.exit()

    a = np.asarray(
        [
            [4, 1, 8, 6, 3, 2, 5, 8, 6, 7],
            [4, 1, 8, 6, 7, 9, 5, 1, 2, 3.6],
            [4, 1, 8, 6, 3, 2, 3, 8, 6, 7],
            [4, 1, 8, 6, 7, 9, 3, 1, 2, 3.6],
        ]
    )

    c = np.asarray([0.1, 0.2, 0.2, 0.4, 0.4, 0.6, 0.3, 0.7, 0.5, 0.5])

    d = np.zeros(10)
    for i in range(10):
        b = (x - a[:, i]) ** 2
        d[i] = sum(b)
    f = -sum((c + d) ** (-1))
    return f


def hm3(x):
    """
    # Hartman3 function
    """
    if len(x) != 3:
        print("Hartman3 function takes only a vector length 3")
        sys.exit()

    a = np.asarray(
        [[3.0, 0.1, 3.0, 0.1], [10.0, 10.0, 10.0, 10.0], [30.0, 35.0, 30.0, 35.0]]
    )

    p = np.asarray(
        [
            [0.36890, 0.46990, 0.10910, 0.03815],
            [0.11700, 0.43870, 0.87320, 0.57430],
            [0.26730, 0.74700, 0.55470, 0.88280],
        ]
    )

    c = np.asarray([1.0, 1.2, 3.0, 3.2])

    d = np.zeros(4)
    for i in range(4):
        d[i] = sum(a[:, i] * np.power((x - p[:, i]), 2))
    f = -sum(c * np.exp(-d))
    return f


def hm6(x):
    """
    # Hartman6 function
    """
    if len(x) != 6:
        print("Hartman6 function takes only a vector length 6")
        sys.exit()

    a = np.asarray(
        [
            [10.00, 0.05, 3.00, 17.00],
            [3.00, 10.00, 3.50, 8.00],
            [17.00, 17.00, 1.70, 0.05],
            [3.50, 0.10, 10.00, 10.00],
            [1.70, 8.00, 17.00, 0.10],
            [8.00, 14.00, 8.00, 14.00],
        ]
    )

    p = np.asarray(
        [
            [0.1312, 0.2329, 0.2348, 0.4047],
            [0.1696, 0.4135, 0.1451, 0.8828],
            [0.5569, 0.8307, 0.3522, 0.8732],
            [0.0124, 0.3736, 0.2883, 0.5743],
            [0.8283, 0.1004, 0.3047, 0.1091],
            [0.5886, 0.9991, 0.6650, 0.0381],
        ]
    )

    c = np.asarray([1.0, 1.2, 3.0, 3.2])

    d = np.zeros(4)
    for i in range(4):
        d[i] = sum(a[:, i] * np.power((x - p[:, i]), 2))
    f = -sum(c * np.exp(-d))
    return f
