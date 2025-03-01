# Documentation for `meteogram`

!["Docs build"](https://readthedocs.org/projects/meteogram/badge/)
!["Latest version"](https://img.shields.io/pypi/v/meteogram)
![Supported Python versions](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fmarhoy%2Fmeteogram%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)

With the `meteogram` package, you can create meteograms for any location in the world. A
meteogram is a graphical representation of meteorological data, typically used to
display weather forecasts. The weather data is provided by the Norwegian Meteorological
Institute (MET).

Here's an example of a cold place with a bit of snow:
![Cold meteogram](images/meteogram_cold.png)

Here's a place with more snow. The different shades of blue
for the percipitation bars indicate the probability of percipitation:
![Snow meteogram](images/meteogram_snow.png)

This is a place with temperatures on both sides of zero. Note that the color of the
temperature line changes from blue to red when the temperature is above zero:
![Zero meteogram](images/meteogram_oslo.png)

Here's a warm place with mostly clear sky:
![Warm meteogram](images/meteogram_warm.png)

The default values generates a small meteogram with 24 hours of forecast data, suitable
for inclusion in e.g. a Home Assistant dashboard:
![Small meteogram](images/meteogram_small.png)
