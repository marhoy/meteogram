import locale as python_locale
import os

import matplotlib.dates
import matplotlib.image
import numpy as np
import scipy.interpolate
import scipy.signal
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.figure import Figure
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.ticker import MaxNLocator

from . import constants
from . import get_weather_data


def meteogram(place=constants.DEFAULT_PLACE,
              hours=constants.DEFAULT_HOURS,
              symbol_interval=constants.DEFAULT_SYMBOL_INTERVAL,
              locale=constants.DEFAULT_LOCALE,
              bgcolor=constants.DEFAULT_BGCOLOR,
              size_x=constants.DEFAULT_SIZE_H,
              size_y=constants.DEFAULT_SIZE_V):
    python_locale.setlocale(python_locale.LC_ALL, locale)

    data = get_weather_data.get_hourly_forecast(place=place)
    data = data[:hours]

    fig_size = (size_x / constants.DEFAULT_DPI,
                size_y / constants.DEFAULT_DPI)
    fig = Figure(figsize=fig_size, dpi=constants.DEFAULT_DPI)
    FigureCanvas(fig)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    fig.set_facecolor(bgcolor)
    ax1.set_facecolor(bgcolor)

    plot_temp(data, ax1)
    format_axes(ax1, ax2)
    plot_precipitation(data, ax2)
    add_weather_symbols(data, ax=ax1, symbol_interval=symbol_interval)
    add_wind_arrows(data, ax=ax1, symbol_interval=symbol_interval)

    return fig


def plot_temp(df, ax):
    t = df['from_mpl'].values
    y = df['temp'].values

    t_fine_res = np.linspace(t[0], t[-1], 1000)
    y_smooth = scipy.signal.savgol_filter(y, 3, 1)
    y_fine_res = scipy.interpolate.interp1d(t, y_smooth, kind='slinear')(t_fine_res)

    df['temp_smoothed'] = y_smooth

    # Create a colormap for red, green and blue and a norm to color
    # f < -0.5 blue, f > 0.5 red
    cmap = ListedColormap(['#007CB2', '#7B3C7B', '#BC1616'])
    norm = BoundaryNorm([-1e3, -.5, .5, 1e3], cmap.N)

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


def plot_precipitation(df, ax):
    t = df['from_mpl']
    y = df['precip']
    y_min = df['precip_min']
    y_max = df['precip_max']

    bars = ax.bar(t, y, align='edge', color='C0', alpha=0.5, width=1 / 24)
    ax.bar(t, y_min, align='edge', color='C0', alpha=0.3, width=1 / 24)
    ax.bar(t, y_max, align='edge', color='C0', alpha=0.2, width=1 / 24)

    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + _pixel_to_units(5, 'v', ax),
                    "{:3.1f}".format(bar.get_height()),
                    ha='center', size='xx-small')


def add_weather_symbols(df, ax, symbol_interval=3):
    for index, row in df.iterrows():
        if divmod(row['from'].hour, symbol_interval)[1] == 0:
            sym = os.path.join(constants.WEATHER_SYMBOLS_DIR, row['symbol'] + '.png')
            img = matplotlib.image.imread(sym, format='png')
            imagebox = OffsetImage(img, zoom=1)
            x_pos = row['from_mpl']
            y_pos = row['temp_smoothed'] + _pixel_to_units(5, 'v', ax)
            ab = AnnotationBbox(imagebox, (x_pos, y_pos), frameon=False, box_alignment=(0.5, 0))
            ax.add_artist(ab)


def add_wind_arrows(df, ax, symbol_interval=3):
    for index, row in df.iterrows():
        if divmod(row['from'].hour, symbol_interval)[1] == 0:
            windspeed_knots = row['wind_speed'] * 3600 / 1852
            windspeed_x = windspeed_knots * np.sin((row['wind_dir'] - 180) / 180 * np.pi)
            windspeed_y = windspeed_knots * np.cos((row['wind_dir'] - 180) / 180 * np.pi)
            x_pos = row['from_mpl']
            y_pos = ax.get_ylim()[0] + _pixel_to_units(20, 'v', ax)
            ax.barbs(x_pos, y_pos, windspeed_x, windspeed_y, length=6, pivot='middle')


def format_axes(ax1, ax2):
    days = matplotlib.dates.DayLocator()
    # noon = matplotlib.dates.HourLocator(byhour=range(12, 24, 12))
    day_format = matplotlib.dates.DateFormatter('%A')
    hours = matplotlib.dates.HourLocator(byhour=range(0, 24, 3))
    hours_format = matplotlib.dates.DateFormatter('%H')
    ax1.xaxis.axis_date()

    # ax1.set_yticks(range(-40, 50, 1), minor=False)
    # ax1.set_yticks(range(-40, 50, 1), minor=True)
    ax1.autoscale()
    ax1.set_ylim(bottom=np.floor(ax1.get_ylim()[0]), top=np.ceil(ax1.get_ylim()[1]))
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax2.set_ylim(bottom=0, top=2)
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax1.xaxis.set_major_locator(days)
    ax1.xaxis.set_major_formatter(day_format)
    ax1.xaxis.set_minor_locator(hours)
    ax1.xaxis.set_minor_formatter(hours_format)

    ax1.xaxis.set_tick_params(which='major', pad=15)
    for label in ax1.xaxis.get_majorticklabels():
        label.set_horizontalalignment('left')

    ax1.grid(which='major', alpha=1, linestyle='--')
    ax1.grid(which='minor', alpha=0.2, linestyle=':')

    if (ax1.get_ylim()[0] < 0) & (ax1.get_ylim()[1] > 0):
        ax1.axhline(0, color='black', linestyle=':', alpha=0.7)

    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    # ax1.set_ylabel('Temperatur [℃]')
    # ax2.set_ylabel('Nedbør [mm/h]')

    ax1.figure.tight_layout(pad=0.2)


def round_base(x, base=5):
    return int(base * np.floor(x / base))


def _get_ax_size_pixels(ax):
    fig = ax.figure
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width = bbox.width * fig.dpi
    height = bbox.height * fig.dpi
    return width, height


def _pixel_to_units(pixels, direction, ax):
    if direction == 'h':
        ax_size_units = ax.get_xlim()[1] - ax.get_xlim()[0]
        ax_size_pixels = _get_ax_size_pixels(ax)[0]
    elif direction == 'v':
        ax_size_units = ax.get_ylim()[1] - ax.get_ylim()[0]
        ax_size_pixels = _get_ax_size_pixels(ax)[1]
    else:
        raise Exception
    units = pixels * ax_size_units / ax_size_pixels
    return units
