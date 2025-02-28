"""REST API."""

import io
from typing import Annotated

from fastapi import FastAPI, Query
from starlette.responses import StreamingResponse

import meteogram
from meteogram.get_weather_data import get_hourly_forecast
from meteogram.schemas import Location


class QueryParams(Location):
    """Query parameters."""

    hours: int | None = None


app = FastAPI()


@app.get("/")
def get_meteogram(query: Annotated[QueryParams, Query()]) -> StreamingResponse:
    """Return a meteogram as a png-image."""
    location = Location.model_validate(query.model_dump())
    data = get_hourly_forecast(location)

    fig = meteogram.meteogram(data, hours=query.hours)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)

    return StreamingResponse(img, media_type="image/png")
