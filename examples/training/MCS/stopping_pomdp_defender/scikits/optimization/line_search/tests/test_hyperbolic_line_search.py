# -*- coding: utf-8 -*-

import unittest
import numpy
from numpy.testing import *
from .. import HyperbolicLineSearch

from .function import Function

class test_HyperbolicLineSearch(unittest.TestCase):
  def test_call_gradient_direction(self):
    lineSearch = HyperbolicLineSearch()
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.array((4., -8.)), 'iteration' : 0}
    function = Function()
    x = lineSearch(origin = numpy.zeros((2)), state = state, function = function)
    assert(state['alpha_step'] > 0)

  def test_call_gradient_direction_with_init(self):
    lineSearch = HyperbolicLineSearch()
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.array((4., -8.)), 'initial_alpha_step' : 1., 'iteration' : 0}
    function = Function()
    x = lineSearch(origin = numpy.zeros((2)), state = state, function = function)
    assert(state['alpha_step'] > 0)

if __name__ == "__main__":
  unittest.main()
