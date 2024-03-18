# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 07:11:44 2019

@author: yl918888
"""

# function f=quartic(a,x);
# evaluates f(x)=a[0]x^4+a[1]x^3+a[2]x^2+a[3]x+a[4]
# simultaneously at a vector x
#
def quartic(a,x):
    return (((a[0]*x + a[1])* x + a[2])* x+a[3])*x+a[4]