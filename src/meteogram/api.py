"""REST API."""

import io

from fastapi import FastAPI
from starlette.responses import StreamingResponse

import meteogram
from meteogram.schemas import Location

app = FastAPI()


@app.get("/")
def get_meteogram(lat: float, lon: float, altitude: int = None):

    location = Location(lat=lat, lon=lon, altitude=altitude)

    fig = meteogram.meteogram(location=location)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)

    return StreamingResponse(img, media_type="image/png")
