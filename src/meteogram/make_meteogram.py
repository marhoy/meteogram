"""Code for creating a meteogram."""

import contextlib
import importlib.resources
import locale as python_locale
from typing import Literal

import matplotlib as mpl
import matplotlib.dates
import matplotlib.image
import numpy as np
import pandas as pd
import scipy.interpolate
import scipy.signal
from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.collections import LineCollection
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.figure import Figure
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.ticker import MaxNLocator

from meteogram import config


def meteogram(
    data: pd.DataFrame,
    hours: int | None = None,
    symbol_interval: int | None = None,
    locale: str | None = None,
    timezone: str | None = None,
    bgcolor: tuple[float, float, float] | None = None,
    size_x: int | None = None,
    size_y: int | None = None,
) -> Figure:
    """Create a meteogram."""
    if hours is None:
        hours = config.HOURS
    if symbol_interval is None:
        symbol_interval = config.SYMBOL_INTERVAL
    if locale is None:
        locale = config.LOCALE
    if timezone is None:
        timezone = config.TIMEZONE
    if bgcolor is None:
        bgcolor = config.BGCOLOR
    if size_x is None:
        size_x = config.HORIZONTAL_SIZE
    if size_y is None:
        size_y = config.VERTICAL_SIZE

    with contextlib.suppress(python_locale.Error):
        python_locale.setlocale(python_locale.LC_ALL, locale)

    # Use only the first n elements. The first element includes the current hour.
    now_1h = pd.Timestamp.utcnow().floor("1h")
    first_datapoint = (data["from"] >= now_1h).argmax()
    last_datapoint = first_datapoint + hours
    data = data.iloc[first_datapoint:last_datapoint].copy()

    # Convert the timestamps to naïve, local timezone
    data["from_local"] = data["from"].dt.tz_convert(timezone).dt.tz_localize(tz=None)
    # Create a new column with a Matplotlib-friendly datetimes
    data["from_mpl"] = matplotlib.dates.date2num(data["from_local"])

    # Set overall font size
    mpl.rc("font", size=14.5)

    # Create the figure canvas and axes
    fig_size = (size_x / config.DPI, size_y / config.DPI)
    fig = Figure(figsize=fig_size, dpi=config.DPI)
    FigureCanvas(fig)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    fig.set_facecolor(bgcolor)
    ax1.set_facecolor(bgcolor)

    # Add things to the axes
    plot_temp(data, ax1)
    format_axes(ax1, ax2)
    plot_precipitation(data, ax2)
    add_weather_symbols(data, ax=ax1, symbol_interval=symbol_interval)
    add_wind_arrows(data, ax=ax1, symbol_interval=symbol_interval)

    return fig


def plot_temp(df: pd.DataFrame, ax: Axes) -> None:
    """Plot temperature."""
    t = df["from_mpl"].to_numpy()
    y = df["temp"].to_numpy()

    t_fine_res = np.linspace(t[0], t[-1], 1000)
    y_smooth = scipy.signal.savgol_filter(y, 3, 1)
    y_fine_res = scipy.interpolate.interp1d(t, y_smooth, kind="slinear")(t_fine_res)

    df["temp_smoothed"] = y_smooth

    # Create a colormap for red, green and blue and a norm to color
    # f < -0.5 blue, f > 0.5 red
    cmap = ListedColormap(["#007CB2", "#7B3C7B", "#BC1616"])
    norm = BoundaryNorm([-1e3, -1, 1, 1e3], cmap.N)

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
    lc.set_linewidth(6)

    ax.add_collection(lc)


def plot_precipitation(df: pd.DataFrame, ax: Axes) -> None:
    """Plot precipitation."""
    t = df["from_mpl"]
    y = df["precip"]
    y_min = df["precip_min"]
    y_max = df["precip_max"]

    bars = ax.bar(t, y, align="edge", color="C0", alpha=0.5, width=1 / 24)
    ax.bar(t, y_min, align="edge", color="C0", alpha=0.3, width=1 / 24)
    ax.bar(t, y_max, align="edge", color="C0", alpha=0.2, width=1 / 24)

    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + _pixel_to_units(5, "v", ax),
                f"{bar.get_height():3.1f}",
                ha="center",
                size="xx-small",
            )


def add_weather_symbols(df: pd.DataFrame, ax: Axes, symbol_interval: int = 3) -> None:
    """Add weather symbols to the meteogram."""
    for _, row in df.iterrows():
        if row["from_local"].hour % symbol_interval == 0:
            with importlib.resources.path(
                "meteogram.weather_symbols.png", f"{row['symbol']}.png"
            ) as file:
                img = matplotlib.image.imread(file, format="png")
            imagebox = OffsetImage(img, zoom=0.20)
            x_pos = row["from_mpl"]
            y_pos = row["temp_smoothed"] + _pixel_to_units(0, "v", ax)
            ab = AnnotationBbox(
                imagebox, (x_pos, y_pos), frameon=False, box_alignment=(0.5, 0)
            )
            ax.add_artist(ab)


def add_wind_arrows(df: pd.DataFrame, ax: Axes, symbol_interval: int = 3) -> None:
    """Add wind arrows to the meteogram."""
    for _, row in df.iterrows():
        if row["from_local"].hour % symbol_interval == 0:
            windspeed_knots = row["wind_speed"] * 3600 / 1852
            windspeed_x = windspeed_knots * np.sin(
                (row["wind_dir"] - 180) / 180 * np.pi
            )
            windspeed_y = windspeed_knots * np.cos(
                (row["wind_dir"] - 180) / 180 * np.pi
            )
            x_pos = row["from_mpl"]
            y_pos = ax.get_ylim()[0] + _pixel_to_units(20, "v", ax)
            ax.barbs(x_pos, y_pos, windspeed_x, windspeed_y, length=7, pivot="middle")


def format_axes(ax1: Axes, ax2: Axes) -> None:
    """Format the axes."""
    days = matplotlib.dates.DayLocator()
    # noon = matplotlib.dates.HourLocator(byhour=range(12, 24, 12))
    day_format = matplotlib.dates.DateFormatter("%A")
    hours = matplotlib.dates.HourLocator(byhour=range(0, 24, 3))
    hours_format = matplotlib.dates.DateFormatter("%H")
    ax1.xaxis.axis_date()

    # ax1.set_yticks(range(-40, 50, 1), minor=False)
    # ax1.set_yticks(range(-40, 50, 1), minor=True)
    ax1.autoscale()
    ax1.set_ylim(bottom=np.floor(ax1.get_ylim()[0]), top=np.ceil(ax1.get_ylim()[1] + 0))
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax2.set_ylim(bottom=0, top=2)
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax1.xaxis.set_major_locator(days)
    ax1.xaxis.set_major_formatter(day_format)
    ax1.xaxis.set_minor_locator(hours)
    ax1.xaxis.set_minor_formatter(hours_format)

    ax1.xaxis.set_tick_params(which="major", pad=15)
    for label in ax1.xaxis.get_majorticklabels():
        label.set_horizontalalignment("left")

    ax1.grid(which="major", alpha=1, linestyle="--")
    ax1.grid(which="minor", alpha=0.2, linestyle=":")

    if (ax1.get_ylim()[0] < 0) & (ax1.get_ylim()[1] > 0):
        ax1.axhline(0, color="black", linestyle=":", alpha=0.7)

    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    # ax1.set_ylabel("Temperatur [°C]")
    # ax2.set_ylabel("Nedbør [mm/h]")

    ax1.figure.tight_layout(pad=0.2)


def round_base(x: float, base: int = 5) -> int:
    """Round a float to the nearest base."""
    return int(base * np.floor(x / base))


def _get_ax_size_pixels(ax: Axes) -> tuple[float, float]:
    fig = ax.figure
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width = bbox.width * fig.dpi
    height = bbox.height * fig.dpi
    return width, height


def _pixel_to_units(pixels: int, direction: Literal["h", "v"], ax: Axes) -> float:
    if direction == "h":
        ax_size_units = ax.get_xlim()[1] - ax.get_xlim()[0]
        ax_size_pixels = _get_ax_size_pixels(ax)[0]
    elif direction == "v":
        ax_size_units = ax.get_ylim()[1] - ax.get_ylim()[0]
        ax_size_pixels = _get_ax_size_pixels(ax)[1]
    else:
        raise Exception
    return pixels * ax_size_units / ax_size_pixels
