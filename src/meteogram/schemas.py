"""API Schemas."""

from pydantic import BaseModel
from pydantic.fields import Field


class Location(BaseModel):
    """Yr location."""

    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    altitude: int | None = Field(default=None, ge=0)
