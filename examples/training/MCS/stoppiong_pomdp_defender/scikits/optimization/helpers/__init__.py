
"""
Helper functions

Fitting functions :
  - Quadratic defines a quadratic cost

NB : the first dimension of the cost, gradient or hessian is the number of points to fit, the second is the dimension of the point if there is one. This leads to the fact that the gradient returns in fact the jacobian of the function.

Finite Difference functions :
  - ForwardFiniteElementDerivatives
  - CenteredFiniteElementDerivatives
"""

from quadratic import *
from levenberg_marquardt import *
from finite_difference import *

helpers__all__ = ['Quadratic', 'ForwardFiniteDifferences', 'CenteredFiniteDifferences']

__all__ = helpers__all__
