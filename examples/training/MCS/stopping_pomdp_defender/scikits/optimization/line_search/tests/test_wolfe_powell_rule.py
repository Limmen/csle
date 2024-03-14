# -*- coding: utf-8 -*-

import unittest
import numpy
from numpy.testing import *
from .. import WolfePowellRule

from .function import Function2 as Function

class test_WolfePowellRuleSearch(unittest.TestCase):
  def test_call(self):
    lineSearch = WolfePowellRule()
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.ones((2))}
    function = Function()
    assert_array_less(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.ones((2)) * 0.0001)
    assert(state['alpha_step'] < 0.0001)

  def test_call_with_init(self):
    lineSearch = WolfePowellRule()
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.ones((2)), 'initial_alpha_step' : 1}
    function = Function()
    assert_array_less(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.ones((2)) * 0.0001)
    assert(state['alpha_step'] < 0.0001)

  def test_call_sigma(self):
    lineSearch = WolfePowellRule(sigma = 1)
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.ones((2))}
    function = Function()
    assert_array_less(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.ones((2)) * 0.0001)
    assert(state['alpha_step'] < 0.0001)

  def test_call_nan(self):
    lineSearch = WolfePowellRule(alpha_min = numpy.nan)
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.ones((2))}
    function = Function()
    assert_array_equal(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.zeros((2)))
    assert(state['alpha_step'] == 0)

  def test_call_gradient_direction(self):
    lineSearch = WolfePowellRule()
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.array((4., -8.))}
    function = Function()
    x = lineSearch(origin = numpy.zeros((2)), state = state, function = function)
    assert(function(x) <= function(numpy.zeros((2)) + 0.1 * state['alpha_step'] * numpy.dot(numpy.array((4., -8.)), numpy.array((4., -8.)))))
    assert(numpy.dot(function.gradient(state['alpha_step'] * numpy.array((4., -8.))).T, numpy.array((4., -8.))) >0.4 * numpy.dot(state['gradient'], numpy.array((4., -8.))))
    assert(state['alpha_step'] > 0)

if __name__ == "__main__":
  unittest.main()
