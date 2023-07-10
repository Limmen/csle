import ternary
import numpy as np
import math

points = []
coefficients = [-3.24, -4.41]
coefficients[0] = 1 + math.pow(coefficients[0], 2)
coefficients[1] = math.pow(coefficients[1], 2)
x = [0, 1, coefficients[-2], coefficients[-1]]

for i in np.linspace(0, 1, 100):
    for j in np.linspace(0, 1 - i, 100):
        k = 1 - i + j
        b = [i, j, k]
        y = [i, j, k, -1]
        d = np.dot(x, y)
        if round(d, 1) == 0:
            points.append([i, j, k])

scale = 1
figure, tax = ternary.figure(scale=scale)

# Draw Boundary and Gridlines
tax.boundary(linewidth=2.0)
tax.gridlines(color="blue", multiple=0.1)

# Set Axis labels and Title
fontsize = 12
offset = 0.14
tax.right_corner_label("healthy (1,0,0)", fontsize=fontsize)
tax.top_corner_label("discovered (0,1,0)", fontsize=fontsize)
tax.left_corner_label("compromised (0,0,1)", fontsize=fontsize)
tax.plot(points, linewidth=2.0, label="Curve")
tax.get_axes().axis('off')
tax.clear_matplotlib_ticks()

tax.show()
