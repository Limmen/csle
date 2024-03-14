# -*- coding: utf-8 -*-

import unittest
import numpy
from numpy.testing import *
from .. import BacktrackingSearch

from .function import Function

class test_BacktrackingSearch(unittest.TestCase):

  def test_call(self):
    lineSearch = BacktrackingSearch()
    state = {'gradient' : numpy.array((4., -8.)), 'direction' : numpy.ones((2))}
    function = Function()
    assert_array_less(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.ones((2)) * 0.0001)
    assert(state['alpha_step'] < 0.0001)

  def test_call_with_init(self):
    lineSearch = BacktrackingSearch()
    state = {'gradient' : numpy.array((4., -8.)), 'direction' : numpy.ones((2)), 'initial_alpha_step' : 1.}
    function = Function()
    assert_array_less(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.ones((2)) * 0.0001)
    assert(state['alpha_step'] < 0.0001)

  def test_call_gradient_direction(self):
    lineSearch = BacktrackingSearch()
    state = {'gradient' : numpy.array((4., -8.)), 'direction' : numpy.array((4., -8.))}
    function = Function()
    x = lineSearch(origin = numpy.zeros((2)), state = state, function = function)
    assert(function(x) <= function(numpy.zeros((2))) + 0.1 * state['alpha_step'] * numpy.dot(numpy.array((4., -8.)), numpy.array((4., -8.))))
    assert(state['alpha_step'] > 0)

if __name__ == "__main__":
  unittest.main()
