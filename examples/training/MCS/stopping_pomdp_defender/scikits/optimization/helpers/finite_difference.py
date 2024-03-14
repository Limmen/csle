
import numpy

class ForwardFiniteDifferences(object):
  """
  A function that will be able to computes its derivatives with a forward difference formula
  """
  def __init__(self, difference = 1e-7, *args, **kwargs):
    """
    Creates the function :
    - difference is the amount of difference that will be used in the computations
    """
    self.difference = difference
    self.inv_difference = 1. / difference

  def gradient(self, params):
    """
    Computes the gradient of the function
    """
    grad = numpy.empty(params.shape)
    current_value = self(params)
    for i in range(0, len(params)):
      paramsb = params.copy()
      paramsb[i] += self.difference
      grad[i] = self.inv_difference * (self(paramsb) - current_value)
    return grad

  def hessian(self, params):
    """
    Computes the hessian of the function
    """
    hess = numpy.empty((len(params), len(params)))
    current_gradient = self.gradient(params)
    for i in range(0, len(params)):
      paramsb = params.copy()
      paramsb[i] -= self.difference
      hess[i] = -self.inv_difference * (self.gradient(paramsb) - current_gradient)
    return hess

  def hessianvect(self, params):
    """
    Computes the hessian times a vector
    """
    NotImplemented

class CenteredFiniteDifferences(object):
  """
  A function that will be able to computes its derivatives with a centered difference formula
  """
  def __init__(self, difference = 1e-7, *args, **kwargs):
    """
    Creates the function :
    - difference is the amount of difference that will be used in the computations
    """
    self.difference = difference
    self.inv_difference = 1. / (2 * difference)

  def gradient(self, params):
    """
    Computes the gradient of the function
    """
    grad = numpy.empty(params.shape)
    for i in range(0, len(params)):
      paramsa = params.copy()
      paramsb = params.copy()
      paramsa[i] -= self.difference
      paramsb[i] += self.difference
      grad[i] = self.inv_difference * (self(paramsb) - self(paramsa))
    return grad

  def hessian(self, params):
    """
    Computes the hessian of the function
    """
    hess = numpy.empty((len(params), len(params)))
    for i in range(0, len(params)):
      paramsa = params.copy()
      paramsb = params.copy()
      paramsa[i] -= self.difference
      paramsb[i] += self.difference
      hess[i] = self.inv_difference * (self.gradient(paramsb) - self.gradient(paramsa))
    return hess

  def hessianvect(self, params):
    """
    Computes the hessian times a vector
    """
    NotImplemented
