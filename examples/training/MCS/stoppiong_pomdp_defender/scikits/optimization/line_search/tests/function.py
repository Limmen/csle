# -*- coding: utf-8 -*-

import numpy

class Function(object):
  def __call__(self, x):
    return (x[0] - 2) ** 2 + (2 * x[1] + 4) ** 2

  def gradient(self, x):
    return numpy.array((2 * (x[0] - 2), 4 * (2 * x[1] + 4)))

class Function2(object):
  def __call__(self, x):
    return (x[0] - 2) ** 3 + (2 * x[1] + 4) ** 2

  def gradient(self, x):
    return numpy.array((3 * (x[0] - 2) ** 2, 4 * (2 * x[1] + 4)))
