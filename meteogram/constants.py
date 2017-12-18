import pkg_resources as _pkg_resources

# YR_URL = 'https://www.yr.no/place/Norway/Oslo/Oslo/Godlia/'

DEFAULT_PLACE = 'Norway/Oslo/Oslo/Godlia'
DEFAULT_HOURS = 18
DEFAULT_SYMBOL_INTERVAL = 3
DEFAULT_LOCALE = 'en_US.UTF-8'

WEATHER_SYMBOLS_DIR = _pkg_resources.resource_filename(__name__, 'weather_symbols')
