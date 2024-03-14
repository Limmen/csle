# -*- coding: utf-8 -*-

import unittest
import numpy
from numpy.testing import *
from .. import CubicInterpolationSearch

from .function import Function

class test_CubicInterpolationSearch(unittest.TestCase):
  def test_create(self):
    lineSearch = CubicInterpolationSearch(min_alpha_step = 0.0001)
    assert_equal(lineSearch.step_size, 1.)

  def test_call(self):
    lineSearch = CubicInterpolationSearch(min_alpha_step = 0.0001)
    function = Function()
    state = {'direction' : numpy.ones((2)), 'new_value' : function(numpy.zeros((2)))}
    assert_array_less(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.ones((2)) * 0.0001)
    assert(state['alpha_step'] < 0.0001)

  def test_call_with_init(self):
    lineSearch = CubicInterpolationSearch(min_alpha_step = 0.0001)
    function = Function()
    state = {'direction' : numpy.ones((2)), 'initial_alpha_step' : 1, 'new_value' : function(numpy.zeros((2)))}
    assert_array_less(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.ones((2)) * 0.0001)
    assert(state['alpha_step'] < 0.0001)

  def test_call_gradient_direction(self):
    lineSearch = CubicInterpolationSearch(min_alpha_step = 0.0001)
    function = Function()
    state = {'direction' : numpy.array((4., -8.)), 'new_value' : function(numpy.zeros((2)))}
    assert_almost_equal(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.array((1.0588, -2.1176)), decimal = 4)
    assert_almost_equal(state['alpha_step'], 1.0588/4, decimal = 4)

if __name__ == "__main__":
  unittest.main()
