"""API Schemas."""

from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field


class Location(BaseModel):
    """Yr location."""

    altitude: Optional[int] = None
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
