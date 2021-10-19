import pkg_resources as _pkg_resources

from .schemas import Location

# ?altitude=132&lat=59.909068&lon=10.8392416

DEFAULT_LOCATION = Location(altitude=32, lat=59.916948, lon=10.728118)
DEFAULT_HOURS = 24
DEFAULT_SYMBOL_INTERVAL = 3
DEFAULT_LOCALE = "C.UTF-8"

WEATHER_SYMBOLS_DIR = _pkg_resources.resource_filename(__name__, "weather_symbols")

DEFAULT_DPI = 100
DEFAULT_SIZE_H = 392
DEFAULT_SIZE_V = 234

DEFAULT_BGCOLOR = (0.95, 0.95, 0.95)
