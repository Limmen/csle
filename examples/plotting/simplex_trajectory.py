import ternary
import numpy as np
import math

points = []
# for i in np.linspace(0,1, 0.1)
# coefficients = [0.6, 1.1]
# coefficients = [-5.4, -4.3]
# coefficients = [-2.5, 1.98]
# coefficients = [-6, 0.58]
# coefficients = [-1, 0.6]
# coefficients = [-4.9, 0.6]
# coefficients = [-0.62, 0.3]
# coefficients = [2.7, 1.16]
# coefficients = [-5.16, 1.18]
# coefficients = [-5.16, 1.18]
# coefficients = [-5.4, -4.3]
coefficients = [-5.4, -4.33]
coefficients = [-5.9, -3.4]
coefficients = [-5.36, 4.19]
coefficients = [-11, 9.45]
coefficients = [-6, -3.7]
coefficients = [-6, -5]
coefficients = [-7, -5]
coefficients = [-7.78833967, -4.21435417]
coefficients = [-0.24, -6.1]
coefficients = [-4.7, -1.51]
coefficients = [-6.5, -5]
coefficients = [-8, 6]
coefficients = [-8.7, 5.6]
coefficients = [-4, 2.5]
coefficients = [-5.7, -4.5]
coefficients[0] = 1 + math.pow(coefficients[0],2)
coefficients[1] = math.pow(coefficients[1],2)

# coefficients = [1.6, 2]
# coefficients = [1.6, 2]
# coefficients = [1.6, 1.3]
print(coefficients)
x = [0,1,coefficients[-2], coefficients[-1]]

for i in np.linspace(0,1, 100):
    for j in np.linspace(0,1-i, 100):
        k = 1-i+j
        b=[i,j,k]
        y = [i,j,k,-1]
        # if round(np.dot(x,y), 1) == 0:
        d = np.dot(x,y)
        # if d <= 0.5 and d >= -0.5:
        if round(d, 1) == 0:
            points.append([i,j,k])
        if d > 0:
            print(b)
# print(points)
scale = 1
figure, tax = ternary.figure(scale=scale)
# figure.set_size_inches(10, 10)

# Draw Boundary and Gridlines
tax.boundary(linewidth=2.0)
tax.gridlines(color="blue", multiple=0.1)

# Set Axis labels and Title
fontsize = 12
offset = 0.14
# tax.set_title(r"$B^{(j)}_{\mathrm{D}}$", fontsize=fontsize)
tax.right_corner_label("healthy (1,0,0)", fontsize=fontsize)
tax.top_corner_label("discovered (0,1,0)", fontsize=fontsize)
tax.left_corner_label("compromised (0,0,1)", fontsize=fontsize)
#tax.left_axis_label("Left label $\\alpha^2$", fontsize=fontsize, offset=offset)
#tax.right_axis_label("Right label $\\beta^2$", fontsize=fontsize, offset=offset)
#tax.bottom_axis_label("Bottom label $\\Gamma - \\Omega$", fontsize=fontsize, offset=offset)

# Draw lines parallel to the axes
# tax.horizontal_line(16)
# tax.left_parallel_line(10, linewidth=2., color='red', linestyle="--")
# tax.right_parallel_line(20, linewidth=3., color='blue')
# Draw an arbitrary line, ternary will project the points for you
# p1 = (22, 8, 10)
# p2 = (2, 22, 16)
# tax.line(p1, p2, linewidth=3., marker='s', color='green', linestyle=":")
tax.plot(points, linewidth=2.0, label="Curve")
# tax.ticks(axis='lbr', multiple=0.1, linewidth=1, offset=0.025)
tax.get_axes().axis('off')
tax.clear_matplotlib_ticks()

tax.show()