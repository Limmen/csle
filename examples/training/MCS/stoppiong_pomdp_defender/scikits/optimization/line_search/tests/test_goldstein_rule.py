# -*- coding: utf-8 -*-

import unittest
import numpy
from numpy.testing import *
from .. import GoldsteinRule

from .function import Function

class test_GoldsteinRuleSearch(unittest.TestCase):
  def test_call_gradient_direction(self):
    lineSearch = GoldsteinRule()
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.array((4., -8.))}
    function = Function()
    x = lineSearch(origin = numpy.zeros((2)), state = state, function = function)
    assert(function(x) <= function(numpy.zeros((2))) + 0.1 * state['alpha_step'] * numpy.dot(numpy.array((12., 16.)), numpy.array((4., -8.))))
    assert(function(x) >= function(numpy.zeros((2))) + 0.9 * state['alpha_step'] * numpy.dot(numpy.array((12., 16.)), numpy.array((4., -8.))))
    assert(state['alpha_step'] > 0)

  def test_call_gradient_direction_bis(self):
    lineSearch = GoldsteinRule(rho = .45)
    state = {'gradient' : numpy.array((11., 17.)), 'direction' : numpy.array((4., -8.))}
    function = Function()
    x = lineSearch(origin = numpy.zeros((2)), state = state, function = function)
    assert(function(x) <= function(numpy.zeros((2))) + 0.1 * state['alpha_step'] * numpy.dot(numpy.array((11., 17.)), numpy.array((4., -8.))))
    assert(function(x) >= function(numpy.zeros((2))) + 0.9 * state['alpha_step'] * numpy.dot(numpy.array((11., 17.)), numpy.array((4., -8.))))
    assert(state['alpha_step'] > 0)

  def test_call_gradient_direction_with_init(self):
    lineSearch = GoldsteinRule()
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.array((4., -8.)), 'initial_alpha_step' : 1}
    function = Function()
    x = lineSearch(origin = numpy.zeros((2)), state = state, function = function)
    assert(function(x) <= function(numpy.zeros((2))) + 0.1 * state['alpha_step'] * numpy.dot(numpy.array((12., 16.)), numpy.array((4., -8.))))
    assert(function(x) >= function(numpy.zeros((2))) + 0.9 * state['alpha_step'] * numpy.dot(numpy.array((12., 16.)), numpy.array((4., -8.))))
    assert(state['alpha_step'] > 0)

  def test_call_nan(self):
    lineSearch = GoldsteinRule(alpha_min = numpy.nan)
    state = {'gradient' : numpy.array((12., 16.)), 'direction' : numpy.array((4., -8.))}
    function = Function()
    x = lineSearch(origin = numpy.zeros((2)), state = state, function = function)
    assert(state['alpha_step'] == 0)

if __name__ == "__main__":
  unittest.main()
