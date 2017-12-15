import matplotlib.pyplot as plt
import numpy as np

from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import scipy.signal
import scipy.interpolate


def plot_temp(t, y, ax=None):
    if ax is None:
        ax = plt.gca()

    t_fine_res = np.linspace(t[0], t[-1], 1000)
    y_smooth = scipy.signal.savgol_filter(y, 5, 0)
    y_fine_res = scipy.interpolate.interp1d(t, y_smooth, kind='cubic')(t_fine_res)

    # Create a colormap for red, green and blue and a norm to color
    # f < -0.5 blue, f > 0.5 red
    cmap = ListedColormap(['b', 'r'])
    norm = BoundaryNorm([0], cmap.N)

    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be numlines x points per line x 2 (x and y)
    points = np.array([t_fine_res, y_fine_res]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create the line collection object, setting the colormapping parameters.
    # Have to set the actual values used for colormapping separately.
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(y_fine_res)
    lc.set_linewidth(3)

    ax.add_collection(lc)
