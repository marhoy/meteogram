import locale as python_locale

import matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import scipy.signal
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.ticker import MaxNLocator

from . import constants
from . import get_weather_data


def meteogram(place=constants.DEFAULT_PLACE, hours=constants.DEFAULT_HOURS,
              symbol_interval=constants.DEFAULT_SYMBOL_INTERVAL, locale=constants.DEFAULT_LOCALE):

    python_locale.setlocale(python_locale.LC_ALL, locale)

    data = get_weather_data.get_hourly_forecast(place=place)
    data = data[:hours]

    fig, ax1 = plt.subplots(1, 1, figsize=(3.92, 2.34))
    ax2 = ax1.twinx()

    plot_temp(data, ax1)
    plot_precipitation(data, ax2)
    format_axes(ax1, ax2)
    add_weather_symbols(data, ax=ax1, symbol_interval=symbol_interval)
    plt.tight_layout(pad=0.2)
    return fig


def plot_temp(df, ax=None):
    if ax is None:
        ax = plt.gca()

    t = df['from_mpl'].values
    y = df['temp'].values

    t_fine_res = np.linspace(t[0], t[-1], 1000)
    y_smooth = scipy.signal.savgol_filter(y, 3, 1)
    y_fine_res = scipy.interpolate.interp1d(t, y_smooth, kind='slinear')(t_fine_res)

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


def plot_precipitation(df, ax=None):
    if ax is None:
        ax = plt.gca()

    t = df['from_mpl']
    y = df['precip']
    y_min = df['precip_min']
    y_max = df['precip_max']

    ax.bar(t, y, align='edge', color='C0', alpha=0.5, width=1 / 24)
    ax.bar(t, y_min, align='edge', color='C0', alpha=0.3, width=1 / 24)
    ax.bar(t, y_max, align='edge', color='C0', alpha=0.2, width=1 / 24)
    ax.set_ylim(bottom=0, top=2)


def add_weather_symbols(df, ax=None, symbol_interval=3):
    if ax is None:
        ax = plt.gca()

    y_pos = ax.get_ylim()[1] - .1 * (ax.get_ylim()[1] - ax.get_ylim()[0])
    for index, row in df.iterrows():
        if divmod(row['from'].hour, symbol_interval)[1] == 0:
            sym = constants.symbol_dir + row['symbol'] + '.png'
            img = plt.imread(sym, format='png')
            imagebox = OffsetImage(img, zoom=1)
            ab = AnnotationBbox(imagebox, (row['from_mpl'] + 0.5/24, y_pos), frameon=False)
            ax.add_artist(ab)


def format_axes(ax1, ax2):
    days = matplotlib.dates.DayLocator()
    noon = matplotlib.dates.HourLocator(byhour=range(12, 24, 12))
    day_format = matplotlib.dates.DateFormatter('%A')
    hours = matplotlib.dates.HourLocator(byhour=range(0, 24, 3))
    hours_format = matplotlib.dates.DateFormatter('%H')
    ax1.xaxis.axis_date()

    # ax1.set_yticks(range(-40, 50, 1), minor=False)
    # ax1.set_yticks(range(-40, 50, 1), minor=True)
    ax1.autoscale()
    ax1.set_ylim(bottom=np.floor(ax1.get_ylim()[0]), top=np.ceil(ax1.get_ylim()[1]))
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax1.xaxis.set_major_locator(days)
    ax1.xaxis.set_major_formatter(day_format)
    ax1.xaxis.set_minor_locator(hours)
    ax1.xaxis.set_minor_formatter(hours_format)
    ax1.xaxis.set_tick_params(which='major', pad=15)
    for label in ax1.xaxis.get_majorticklabels():
        label.set_horizontalalignment('left')

    ax1.grid(which='major', alpha=1, linestyle='--')
    ax1.grid(which='minor', alpha=0.2, linestyle=':')
    ax1.axhline(0, color='black', linestyle=':', alpha=0.7)

    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    ax1.set_ylabel('Temperatur [℃]')
    ax2.set_ylabel('Nedbør [mm/h]')
