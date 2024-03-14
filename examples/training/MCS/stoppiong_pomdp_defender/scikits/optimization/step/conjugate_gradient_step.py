# -*- coding: utf-8 -*-

"""
Computes the conjugate gradient steps for a specific function at a specific point

The different available gradient are:
- FRConjugateGradientStep: Fletcher-Reeves
- CWConjugateGradientStep: Crowder-Wolfe or Hestenes-Stiefel
- DConjugateGradientStep: Dixon
- DYConjugateGradientStep: Dai Yan
- PRPConjugateGradientStep: Polak-Ribiere-Polyak
- FRPRPConjugateGradientStep: Fletcher-Reeves modified Polak-Ribiere-Polyak
- HZConjugateGradientStep: Hager-Zhang
"""

import numpy

class ConjugateGradientStep(object):
  """
  The basic conjugate gradient step
  """
  def __init__(self, coeff_function):
    """
    Initialization of the gradient step
      - coeff_function is the function that will compute the appropriate coefficient
    """
    self.old_step = None
    self.old_gradient = None
    self.coeff_function = coeff_function

  def __call__(self, function, point, state):
    """
    Computes a gradient step based on a function and a point
    """
    new_gradient = function.gradient(point)

    if 'direction' in state:
      old_gradient = state['gradient']
      old_step = state['direction']
      coeff = self.coeff_function(new_gradient, old_gradient, old_step)
      step = - new_gradient + coeff * old_step
    else:
      coeff = 0
      step = - new_gradient
    self.old_gradient = new_gradient
    state['gradient'] = new_gradient
    state['conjugate_coefficient'] = coeff
    state['direction'] = step
    return step

def CWConjugateGradientStep():
  """
  The Crowder-Wolfe or Hestenes-Stiefel conjugate gradient step
  """
  def function(new_gradient, old_gradient, old_step):
    return numpy.dot(new_gradient.T, (new_gradient - old_gradient)) / numpy.dot(old_step.T, (new_gradient - old_gradient))
  return ConjugateGradientStep(function)

def DConjugateGradientStep():
  """
  The Dixon conjugate gradient step
  """
  def function(new_gradient, old_gradient, old_step):
    return - numpy.dot(new_gradient.T, new_gradient) / numpy.dot(old_step.T, old_gradient)
  return ConjugateGradientStep(function)

def DYConjugateGradientStep():
  """
  The Dai Yan conjugate gradient step
  Has good convergence capabilities (same as the FR-PRP gradient)
  """
  def function(new_gradient, old_gradient, old_step):
    return numpy.dot(new_gradient.T, new_gradient) / numpy.dot(old_step.T, (new_gradient - old_gradient))
  return ConjugateGradientStep(function)

def FRConjugateGradientStep():
  """
  The Fletcher Reeves conjugate gradient step
  Needs an exact line search for convergence or the strong Wolfe-Powell rules for an inexact line search
  """
  def function(new_gradient, old_gradient, old_step):
    return numpy.dot(new_gradient.T, new_gradient) / numpy.dot(old_gradient.T, old_gradient)
  return ConjugateGradientStep(function)

def PRPConjugateGradientStep():
  """
  The Polak-Ribiere-Polyak conjugate gradient step
  Can restart automatically, but needs an exact line search with a uniformely convex function to globally converge
  """
  def function(new_gradient, old_gradient, old_step):
    return numpy.dot(new_gradient.T, (new_gradient - old_gradient)) / numpy.dot(old_gradient.T, old_gradient)
  return ConjugateGradientStep(function)

def FRPRPConjugateGradientStep():
  """
  The Fletcher-Reeves modified Polak-Ribiere-Polyak conjugate gradient step
  Can restart automatically and has the advantages of the PRP gradient and of the FR gradient
  """
  def function(new_gradient, old_gradient, old_step):
    beta = numpy.dot(new_gradient.T, (new_gradient - old_gradient)) / numpy.dot(old_gradient.T, old_gradient)
    betafr = numpy.dot(new_gradient.T, new_gradient) / numpy.dot(old_gradient.T, old_gradient)
    if beta < -betafr:
      beta = -betafr
    elif beta > betafr:
      beta = betafr
    return beta
  return ConjugateGradientStep(function)

def HZConjugateGradientStep():
  """
  The Hager-Zhang conjugate gradient step
  Has good convergence capabilities (same as the FR-PRP gradient)
  """
  def function(new_gradient, old_gradient, old_step):
    yk = new_gradient - old_gradient
    beta = numpy.dot((yk - 2*numpy.linalg.norm(yk)/numpy.dot(yk.T, old_step) * old_step).T, new_gradient) / numpy.dot(yk.T, old_step)
    return beta
  return ConjugateGradientStep(function)
