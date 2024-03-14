
import unittest
import numpy
from numpy.testing import *

from nose.tools import raises

from ..optimizer import Optimizer

def fun(x):
  return (x[0] - 2) ** 2 + (2 * x[1] + 4) ** 2

def gradient(x):
  return numpy.array((2 * (x[0] - 2), 4 * (2 * x[1] + 4)))

class TestOptimizer(unittest.TestCase):
  def test_function_object(self):
    optimizer = Optimizer(criterion = None, fun = fun, gradient = gradient)
    optimizer.function((0, 0))

  @raises(RuntimeError)
  def test_optimize(self):
    optimizer = Optimizer(criterion = None, fun = fun, gradient = gradient)
    optimizer.optimize()
