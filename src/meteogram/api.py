"""REST API."""

import io

import fastapi
import pydantic
from fastapi import FastAPI
from starlette.responses import StreamingResponse

import meteogram
from meteogram.get_weather_data import get_hourly_forecast
from meteogram.schemas import Location

app = FastAPI()


@app.get("/")
def get_meteogram(lat: float, lon: float, altitude: int = None, hours: int = None):

    try:
        location = Location(lat=lat, lon=lon, altitude=altitude)
    except pydantic.ValidationError:
        raise fastapi.HTTPException(
            status_code=422,
            detail=f"Illegal location: Latitude {lat}, Longitude {lon}",
        )

    data = get_hourly_forecast(location)

    fig = meteogram.meteogram(data, hours=hours)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)

    return StreamingResponse(img, media_type="image/png")
