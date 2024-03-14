#!/usr/bin/env python

import numpy as np
from scikits.optimization import defaults

"""from scikits.optimization import (
    criterion,
    defaults,
    helpers,
    line_search,
    optimizer,
    step,
)"""

# import criterion
# import defaults
# import helperss
# import line_search
# import optimizer
# import step
from scikits.optimization.optimizer import optimizer


class MCS(optimizer.Optimizer):
    """A Multilevel Coordinate Search"""

    def __init__(self, **kwargs):
        """
        Needs to have :
          - an object function to optimize (function), alternatively a function ('fun'), gradient ('gradient'), ...
          - a criterion to stop the optimization (criterion)
          - the two corners of bound box (2 points of dimension n, u, v)
          - optionally the starting point (1 point of dimension n, x0, default is u+v/2)
          - optionally 3 starting points (3 point of dimension n, x, default is x0,u,v)
          - optionally the maximum search level (1 float, default is smax=50*n)
        """
        optimizer.Optimizer.__init__(self, **kwargs)

        self.bound1 = kwargs["u"]
        self.bound2 = kwargs["v"]
        if "x0" not in kwargs:
            if "x" in kwargs:
                self.optimal_parameters = list(kwargs["x"])
            else:
                self.optimal_parameters = [
                    (self.bound1 + self.bound2) / 2,
                    self.bound1,
                    self.bound2,
                ]
        else:
            self.optimal_parameters = [kwargs["x0"], self.bound1, self.bound2]
        self.smax = kwargs.get("smax", 50 * len(self.bound1))

        self.optimal_values = [self.function(x) for x in self.optimal_parameters]
        self.initialize_box()
        print(self.optimal_values)
        best = np.argmin(self.optimal_values)
        self.state["best_parameters"] = self.optimal_parameters[best]
        self.state["best_value"] = self.optimal_values[best]

        self.record_history(**self.state)

    def initialize_box(self):
        """This methods first computes all the interesting points passed as parameters and then creates the first boxes for the algorithm"""
        x0, f0 = self.initialize_x()
        self.optimal_parameters.append(x0)
        self.optimal_values.append(f0)
        # self.initialize_splitting()

    def initialize_x(self):
        """after starting with a given x, the method adds also to the mix new other points based on the initial distribution"""
        x0 = np.array(self.optimal_parameters[0])
        f0 = self.optimal_values[0]

        for i in range(len(x0)):
            best = 0
            for j in range(1, len(self.optimal_parameters)):
                x0[i] = self.optimal_parameters[j][i]
                f1 = self.function(x0)
                if f1 < f0:
                    best = j
                    f1 = f0
            x0[i] = self.optimal_parameters[best][i]
        return x0, f1

    def optimize(self):
        return self.state["best_parameters"]


class Rosenbrock(object):
    """
    The Rosenbrock function
    """

    def __init__(self):
        self.count = 0

    def __call__(self, x):
        """
        Get the value of the Rosenbrock function at a specific point
        """
        self.count = self.count + 1
        return np.sum(100.0 * (x[1:] - x[:-1] ** 2.0) ** 2.0 + (1.0 - x[:-1]) ** 2.0)


if __name__ == "__main__":
    from numpy.testing import *

    startPoint = np.array((-1.01, 1.01), np.float)
    u = np.array((-2.0, -2.0), np.float)
    v = np.array((2.0, 2.0), np.float)

    optimi = MCS(
        function=Rosenbrock(),
        criterion=criterion.OrComposition(
            criterion.MonotonyCriterion(0.00001), criterion.IterationCriterion(10000)
        ),
        x0=startPoint,
        u=u,
        v=v,
    )
    assert_almost_equal(optimi.optimize(), np.ones(2, np.float), decimal=1)
