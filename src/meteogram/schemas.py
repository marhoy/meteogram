"""API Schemas."""

from pydantic import BaseModel
from pydantic.fields import Field


class Location(BaseModel):
    """A location somewhere in the world."""

    lat: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitude in degrees (North is positive, South is negative)",
    )
    lon: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitude in degrees (East is positive, West is negative)",
    )
    altitude: int | None = Field(
        default=None,
        ge=0,
        description="Altitude above sea level in meters",
    )
