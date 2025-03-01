"""Package wide configuration."""

from pydantic_settings import BaseSettings

from .schemas import Location


class Config(BaseSettings):
    """Config class."""

    # Default location: Norwegian Royal Castle
    LOCATION: Location = Location(lat=59.916948, lon=10.728118, altitude=32)

    TIMEZONE: str = "Europe/Oslo"
    LOCALE: str = "no_NO.UTF-8"

    HOURS: int = 24
    SYMBOL_INTERVAL: int = 3

    DPI: int = 72

    # Cell size is 114 x 114, spacing is 5
    HORIZONTAL_SIZE: int = 114 * 3 + 5 * 2
    VERTICAL_SIZE: int = 114 * 2 + 5 * 1

    BGCOLOR: tuple[float, float, float] = (0.95, 0.95, 0.95)


config = Config()
