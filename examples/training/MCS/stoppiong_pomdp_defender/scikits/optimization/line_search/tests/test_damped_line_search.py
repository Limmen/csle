# -*- coding: utf-8 -*-

import unittest
import numpy
from numpy.testing import *
from .. import DampedLineSearch

from .function import Function

class test_DampedLineSearch(unittest.TestCase):
  def test_create(self):
    lineSearch = DampedLineSearch(min_alpha_step = 0.0001, damped_error = 1.)
    assert_equal(lineSearch.step_size, 1.)

  def test_call(self):
    lineSearch = DampedLineSearch(min_alpha_step = 0.0001, damped_error = 0.1)
    state = {'direction' : numpy.ones((2))}
    function = Function()
    assert_equal(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.ones((2)) * 0.125)
    assert_equal(state['alpha_step'], 0.125)

  def test_call_with_init(self):
    lineSearch = DampedLineSearch(min_alpha_step = 0.0001, damped_error = 0.1)
    state = {'direction' : numpy.ones((2)), 'initial_alpha_step' : 1.}
    function = Function()
    assert_equal(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.ones((2)) * 0.125)
    assert_equal(state['alpha_step'], 0.125)

  def test_call_damped(self):
    lineSearch = DampedLineSearch(min_alpha_step = 0.0001, damped_error = 1.)
    state = {'direction' : numpy.ones((2))}
    function = Function()
    assert_equal(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.ones((2)))
    assert_equal(state['alpha_step'], 1.)

  def test_call_gradient_direction(self):
    lineSearch = DampedLineSearch(min_alpha_step = 0.0001, damped_error = 0.1)
    state = {'direction' : numpy.array((4, -8))}
    function = Function()
    assert_equal(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.array((2, -4)))
    assert_equal(state['alpha_step'], 0.5)

  def test_call_small_step(self):
    lineSearch = DampedLineSearch(min_alpha_step = 0.2, damped_error = 0.1)
    state = {'direction' : numpy.ones((2))}
    function = Function()
    assert_equal(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.zeros((2)))
    assert_equal(state['alpha_step'], 0.)

if __name__ == "__main__":
  unittest.main()