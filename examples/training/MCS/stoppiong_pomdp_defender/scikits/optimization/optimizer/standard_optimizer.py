
"""
A standard optimizer
"""

import optimizer

class StandardOptimizer(optimizer.Optimizer):
  """
  A standard optimizer, takes a step and finds the best candidate
  Must give in self.optimal_point the optimal point after optimization
  """
  def __init__(self, **kwargs):
    """
    Needs to have :
      - an object function to optimize (function), alternatively a function ('fun'), gradient ('gradient'), ...
      - a way to get a new point, that is a step (step)
      - a criterion to stop the optimization (criterion)
      - a starting point (x0)
      - a way to find the best point on a line (line_search)
    Can have :
      - a step modifier, a factor to modulate the step (stepSize = 1.)
    """
    optimizer.Optimizer.__init__(self, **kwargs)
    self.step = kwargs['step']
    self.optimal_point = kwargs['x0']
    self.line_search = kwargs['line_search']

    self.state['new_parameters'] = self.optimal_point
    self.state['new_value'] = self.function(self.optimal_point)

    self.record_history(**self.state)

  def iterate(self):
    """
    Implementation of the optimization. Does one iteration
    """
    step = self.step(self.function, self.optimal_point, state = self.state)
    self.optimal_point = self.line_search(origin = self.optimal_point, function = self.function, state = self.state)
    self.state['old_parameters'] = self.state['new_parameters']
    self.state['old_value'] = self.state['new_value']
    self.state['new_parameters'] = self.optimal_point
    self.state['new_value'] = self.function(self.optimal_point)

    self.record_history(**self.state)

