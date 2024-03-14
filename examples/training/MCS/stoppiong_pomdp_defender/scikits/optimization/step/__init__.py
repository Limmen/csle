
"""
Module containing every step use to lower a cost function

Steps :
  - GradientStep
    - compute a step based on the gradient of the function
  - CWConjugateGradient
    - Crowder-Wolfe conjugate gradient
  - DYConjugateGradient
    - Dai-Yuan conjugate gradient
  - DConjugateGradient
    - Dixon conjugate gradient
  - FRConjugateGradient
    - Fletcher-Reeves conjugate gradient
  - PRPConjugateGradient
    - Polak-Ribiere-Polyak conjugate gradient
  - FRPRPConjugateGradient
    - Fletcher-Reeves modified Polak-Ribiere-Polyak conjugate gradient

  - NewtonStep
    - computes a step based on the hessian and the gradient of the function
  - MarquardtStep
    - computes a step based on the Marquardt modified hessian and the gradient of the function
  - GoldsteinPriceStep
    - computes a step based on the Goldstein-Price Newton modification
  - GoldfeldStep
    - computes a step based on the Goldfeld Newton modification
  - DFPNewtonStep
    - computes a step based on the Davidson-Fletcher-Powell approximation of the hessian
  - BFGSNewtonStep
    - computes a step based on the Broyden-Fletcher-Goldfarb-Shanno approximation of the hessian

  - PartialStep
    - decorator for another step but uses only part of this step
  - RestartPeriodicallyConjugateGradientStep
    - decorator for a conjugate gradient step that restarts the conjugation each n iterations
  - RestartNotOrthogonalConjugateGradientStep
    - decorator for a conjugate gradient step that restarts the conjugation if the last gradients are not orthogonal enough
"""

from gradient_step import *
from conjugate_gradient_step import *

from newton_step import *
from marquardt_step import *
from quasi_newton_step import *
from goldfeld_step import *
from goldstein_price_step import *

from partial_step import *
from restart_conjugate_gradient import *

step__all__ = ['GradientStep',
               'CWConjugateGradientStep', 'DYConjugateGradientStep', 'DConjugateGradientStep', 'FRConjugateGradientStep', 'PRPConjugateGradientStep', 'FRPRPConjugateGradientStep',
               'NewtonStep', 'MarquardtStep', 'GoldsteinPriceStep', 'GoldfeldStep',
               'PartialStep',
               'DFPNewtonStep', 'BFGSNewtonStep',
               'RestartPeriodicallyConjugateGradientStep', 'RestartNotOrthogonalConjugateGradientStep', ]

__all__ = step__all__
