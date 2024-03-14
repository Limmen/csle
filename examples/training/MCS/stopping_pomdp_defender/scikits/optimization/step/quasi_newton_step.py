
"""
Computes a quasi-Newton step for a specific function at a specific point
"""

import numpy
import numpy.linalg

class DFPNewtonStep(object):
  """
  The Davidson-Fletcher-Powell Quasi-Newton step
  """
  def __init__(self, hessian_approx):
    """
    Construct a DFP module
      - hessian_approx is an approximation of the hessian around the starting point
    """
    self.H0 = numpy.linalg.inv(hessian_approx)

  def __call__(self, function, point, state):
    """
    Computes a direction step based on a function and a point
    """
    if 'Hk' not in state:
      Hk = self.H0.copy()
      gradient = function.gradient(point)
    else:
      Hk = state['Hk']
      oldParams = state['old_parameters']
      newParams = state['new_parameters']
      gradient = function.gradient(point)
      oldGradient = state['gradient']

      yk = gradient - oldGradient
      sk = newParams - oldParams
      rho = 1 / numpy.dot(yk.T, sk)
      tk = numpy.dot(Hk, yk)
      Hk = Hk - numpy.outer(tk, tk) / numpy.dot(yk.T, tk) + numpy.outer(sk, sk) / rho

    step = -numpy.dot(Hk, gradient)

    state['Hk'] = Hk
    state['gradient'] = gradient
    state['direction'] = step
    return step

class BFGSNewtonStep(object):
  """
  The Broyden-Fletcher-Goldfarb-Shanno Quasi-Newton step
  """
  def __init__(self, hessian_approx):
    """
    Construct a BFGS module
      - hessian_approx is an approximation of the hessian around the starting point
    """
    self.H0 = numpy.linalg.inv(hessian_approx)

  def __call__(self, function, point, state):
    """
    Computes a direction step based on a function and a point
    """
    if 'Hk' not in state:
      Hk = self.H0.copy()
      gradient = function.gradient(point)
    else:
      Hk = state['Hk']
      oldParams = state['old_parameters']
      newParams = state['new_parameters']
      gradient = function.gradient(point)
      oldGradient = state['gradient']

      yk = gradient - oldGradient
      sk = newParams - oldParams
      rho = 1 / numpy.dot(yk.T, sk)
      fac1 = numpy.eye(len(gradient)) - rho * numpy.outer(sk, yk)
      Hk = numpy.dot(fac1,  numpy.dot(Hk, fac1.T)) + rho * numpy.outer(sk, sk)

    step = -numpy.dot(Hk, gradient)

    state['Hk'] = Hk
    state['gradient'] = gradient
    state['direction'] = step
    return step

class SR1NewtonStep(object):
  """
  The SR1 Quasi-Newton step
  """
  def __init__(self, hessian_approx):
    """
    Construct a SR1 module
      - hessian_approx is an approximation of the hessian around the starting point
    """
    self.H0 = numpy.linalg.inv(hessian_approx)

  def __call__(self, function, point, state):
    """
    Computes a direction step based on a function and a point
    """
    if 'Hk' not in state:
      Hk = self.H0.copy()
      gradient = function.gradient(point)
    else:
      Hk = state['Hk']
      oldParams = state['old_parameters']
      newParams = state['new_parameters']
      gradient = function.gradient(point)
      oldGradient = state['gradient']

      yk = gradient - oldGradient
      sk = newParams - oldParams
      fac1 = sk - numpy.dot(Hk, yk)
      Hk = Hk + numpy.outer(fac1, fac1) / numpy.dot(fac1, yk)

    step = -numpy.dot(Hk, gradient)

    state['Hk'] = Hk
    state['gradient'] = gradient
    state['direction'] = step
    return step

class BroydenNewtonStep(object):
  """
  The Broyden Quasi-Newton step
  """
  def __init__(self, hessian_approx, phi = .5):
    """
    Construct a SR1 module
      - hessian_approx is an approximation of the hessian around the starting point
      - phi = .5 is the weight between DFQ and BFGS Hessian update
    """
    self.B0 = hessian_approx
    self.phi = phi

  def __call__(self, function, point, state):
    """
    Computes a direction step based on a function and a point
    """

    if 'Bk' not in state:
      Bk = self.B0.copy()
      gradient = function.gradient(point)
      hessian = Bk
    else:
      Bk = state['Bk']
      oldParams = state['old_parameters']
      newParams = state['new_parameters']
      gradient = function.gradient(point)
      oldGradient = state['gradient']

      yk = gradient - oldGradient
      sk = newParams - oldParams
      rho = 1 / numpy.dot(yk.T, sk)
      tk = numpy.dot(Bk, sk)
      BkBFGS = Bk - numpy.outer(tk, tk) / numpy.dot(sk.T, tk) + numpy.outer(yk, yk) / rho
      fac1 = numpy.eye(len(gradient)) - rho * numpy.outer(yk, sk)
      BkDFQ = numpy.dot(fac1,  numpy.dot(Bk, fac1.T)) + rho * numpy.outer(yk, yk)
      hessian = (1 - self.phi) * BkBFGS + self.phi * BkDFQ

    step = (-numpy.linalg.solve(hessian, gradient)).reshape(point.shape)

    state['Bk'] = Bk
    state['gradient'] = gradient
    state['direction'] = step
    return step
