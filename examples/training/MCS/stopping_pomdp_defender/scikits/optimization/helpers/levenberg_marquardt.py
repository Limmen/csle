
import quadratic
import numpy

class LMQuadratic(quadratic.Quadratic):
  """
  Defines a cost function with a quadratic cost but the Levenberg-Marquardt approximation of the hessian
  """
  def hessian(self, params):
    """
    Compute sthe hessian of the fit function
    """
    inter = 2 * self.f.gradient(self.x, params)[..., numpy.newaxis] * self.f.gradient(self.x, params)[..., numpy.newaxis, :]
    inter = numpy.ascontiguousarray(inter)
    shape = inter.shape[-2], inter.shape[-1]
    inter.shape = (-1, inter.shape[-2] * inter.shape[-1])
    temp = numpy.sum(inter, axis = 0)
    temp.shape = shape
    return temp