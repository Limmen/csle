# -*- coding: utf-8 -*-

import unittest
import numpy
from numpy.testing import *
from .. import StrongWolfePowellRule

from .function import Function

class test_StrongWolfePowellRuleSearch(unittest.TestCase):
  def test_call_sigma(self):
    lineSearch = StrongWolfePowellRule(sigma = 1)
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.array((4., -8.))}
    function = Function()
    l = lineSearch(origin = numpy.zeros((2)), state = state, function = function)
    assert(2 * l[0] + l[1] == 0)
    assert(state['alpha_step'] > 0)

  def test_call_gradient_direction_with_init(self):
    lineSearch = StrongWolfePowellRule()
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.array((4., -8.)), 'initial_alpha_step' : 1}
    function = Function()
    x = lineSearch(origin = numpy.zeros((2)), state = state, function = function)
    assert(function(x) <= function(numpy.zeros((2))) + 0.1 * state['alpha_step'] * numpy.dot(numpy.array((12., 16.)), numpy.array((4., -8.))))
    assert(numpy.dot(function.gradient(state['alpha_step'] * numpy.array((4., -8.))).T, numpy.array((4., -8.))) >0.4 * numpy.dot(state['gradient'], numpy.array((4., -8.))))
    assert(state['alpha_step'] > 0)

  def test_call_nan(self):
    lineSearch = StrongWolfePowellRule(alpha_min = numpy.nan)
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.ones((2))}
    function = Function()
    assert_array_equal(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.zeros((2)))
    assert(state['alpha_step'] == 0)

  def test_call_gradient_direction(self):
    lineSearch = StrongWolfePowellRule()
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.array((4., -8.))}
    function = Function()
    x = lineSearch(origin = numpy.zeros((2)), state = state, function = function)
    assert(function(x) <= function(numpy.zeros((2))) + 0.1 * state['alpha_step'] * numpy.dot(numpy.array((12., 16.)), numpy.array((4., -8.))))
    assert(numpy.dot(function.gradient(state['alpha_step'] * numpy.array((4., -8.))).T, numpy.array((4., -8.))) >0.4 * numpy.dot(state['gradient'], numpy.array((4., -8.))))
    assert(state['alpha_step'] > 0)

if __name__ == "__main__":
  unittest.main()
