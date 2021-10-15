from pydantic import BaseModel
from pydantic.fields import Field
from typing import Optional


class Location(BaseModel):
    altitude: Optional[int] = None
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
