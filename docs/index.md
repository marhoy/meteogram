# Documentation for `meteogram`

!["Docs build"](https://readthedocs.org/projects/meteogram/badge/)
!["Latest version"](https://img.shields.io/pypi/v/meteogram)
![Supported Python versions](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fmarhoy%2Fmeteogram%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)

With the `meteogram` package, you can create meteograms for any location in the world. A
meteogram is a graphical representation of meteorological data, typically used to
display weather forecasts. The weather data is provided by the Norwegian Meteorological
Institute (MET).

Here's an example with some percipitation, mostly as rain. The different shades of blue
for the percipitation bars indicate the probability of percipitation:

![Example meteogram](images/example_meteogram.png)

For a more sunny and warm location, the meteogram might look like this:

![Example meteogram](images/example_meteogram_warm.png)

The default values generates a small meteogram with 24 hours of forecast data, suitable
for inclusion in e.g. a Home Assistant dashboard:

![Example meteogram](images/example_meteogram_default.png)
