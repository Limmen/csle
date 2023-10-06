import cma
import numpy as np
from numpy.typing import NDArray


def J(x: NDArray):
    return (x[0] - 1)**2 + (x[1] - 7)**2

x_0 = np.ndarray((1, 2))
x_0[0,0] = -2
x_0[0,1] = -3
print(x_0[0,0])
print(x_0[0,1])
es = cma.CMAEvolutionStrategy(x_0, 0.01)
es.optimize(J)
# es.result_pretty() 