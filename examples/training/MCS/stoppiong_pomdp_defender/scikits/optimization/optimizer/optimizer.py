
"""
The core optimizer from which every other optimizer is derived
"""

class Optimizer(object):
  """
  The simple optimizer class
  This class lacks some intel that must be populated/implemented in the subclasses :
    - current_values is a list of the 2 last cost values computed with the function
    - current_parameters is a list of the 2 last parameters used for the computation of currentValues
    - the iterate function that does the real iteration loop
  """
  def __init__(self, **kwargs):
    """
    Initialization of the optimizer, saves the function and the criterion to use
    Needs to have :
      - a function to optimize (function)
      - a criterion to stop the optimization (criterion)
    Can have :
      - a step modifier, a factor to modulate the step (stepSize = 1.)
      - a recorder that will be called with the factors used in one iteration step (record = self.recordHistory)
    """
    # The global state of the optimizer, is passed to every sub module
    self.state = {}

    self.state['iteration'] = -1
    self.optimized = False

    if 'function' in kwargs:
      self.function = kwargs['function']
    else:
      class Function(object):
        def __call__(self, *args, **kwargs):
          self.fun(*args, **kwargs)

      self.function = Function()
      self.function.__dict__.update(kwargs)

    self.state['function'] = self.function
    self.criterion = kwargs['criterion']
    self.record_history = kwargs.get('record', self.record_history)
    self.check_arguments()

  def optimize(self):
    """
    Does the optimization, call iterate and returns the optimal set of parameters
    """
    if not self.optimized:
      self.state['iteration'] = 0
      self.iterate() # needed because we need a do while loop
      self.state['iteration'] += 1
      while(not self.criterion(self.state)):
        self.iterate()
        self.state['iteration'] += 1

      self.optimized = True

    return self.state['new_parameters']

  def record_history(self, **kwargs):
    """
    Function that does nothing, called for saving parameters in the iteration loop, if needed
    """
    pass

  def iterate(self):
    """
    Does one iteration of the optimization
    Present here for readability
    """
    raise RuntimeError("This method should be overrridden")

  def check_arguments(self):
    """
    Checks if the given arguments are correct
    """
    if not hasattr(self.function, 'hessianvect'):
      self.function.hessianvect = lambda x, v: numpy.dot(self.function.hessian(x), v)
