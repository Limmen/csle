import numpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib import colors as mcolors

import random

def gen_data(xbins, numplots, lintest=False):
    """Generate a list of random histograms"""
    data = []
    ymin = 9999999999999
    ymax = -ymin
    for plot in range(numplots):
        plotpoints = []
        y = random.randint(0, 5)
        for x in range(xbins):
            # Optional: instead of random data, make each plot a constant
            # to make it easier to tell which plot is which.
            # Even if lintest isn't set, make the last 20% of the
            # data predictable, to test whether matplotlib3d is
            # re-ordering the plots (it isn't).
            if lintest or x > xbins * .8:
                y = plot
            else:
                y += random.uniform(-.8, 1)
            ymin = min(ymin, y)
            ymax = max(ymax, y)
            plotpoints.append((x, y))
        data.append(plotpoints)

    return data, ymin, ymax

def draw_3d(verts, ymin, ymax, line_at_zero=True, colors=True):
    """Given verts as a list of plots, each plot being a list
       of (x, y) vertices, generate a 3-d figure where each plot
       is shown as a translucent polygon.
       If line_at_zero, a line will be drawn through the zero point
       of each plot, otherwise the baseline will be at the bottom of
       the plot regardless of where the zero line is.
    """
    # add_collection3d() wants a collection of closed polygons;
    # each polygon needs a base and won't generate it automatically.
    # So for each subplot, add a base at ymin.
    if line_at_zero:
        zeroline = 0
    else:
        zeroline = ymin
    for p in verts:
        p.insert(0, (p[0][0], zeroline))
        p.append((p[-1][0], zeroline))

    if colors:
        # All the matplotlib color sampling examples I can find,
        # like cm.rainbow/linspace, make adjacent colors similar,
        # the exact opposite of what most people would want.
        # So cycle hue manually.
        hue = 0
        huejump = .27
        facecolors = []
        edgecolors = []
        for v in verts:
            hue = (hue + huejump) % 1
            c = mcolors.hsv_to_rgb([hue, 1, 1])
                                    # random.uniform(.8, 1),
                                    # random.uniform(.7, 1)])
            edgecolors.append(c)
            # Make the facecolor translucent:
            facecolors.append(mcolors.to_rgba(c, alpha=.7))
    else:
        facecolors = (1, 1, 1, .8)
        edgecolors = (0, 0, 1, 1)

    poly = PolyCollection(verts,
                          facecolors=facecolors, edgecolors=edgecolors)

    zs = range(len(data))
    # zs = range(len(data)-1, -1, -1)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')

    plt.tight_layout(pad=2.0, w_pad=10.0, h_pad=3.0)

    ax.add_collection3d(poly, zs=zs, zdir='y')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_xlim3d(0, len(data[1]))
    ax.set_ylim3d(-1, len(data))
    ax.set_zlim3d(ymin, ymax)

    fig.savefig("hparam_tuning_3" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)


if __name__ == '__main__':
    data, ymin, ymax = gen_data(50, 5, lintest=False)
    draw_3d(data, ymin, ymax, colors=False)