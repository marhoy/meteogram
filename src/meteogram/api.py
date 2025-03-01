"""REST API."""

import io
from typing import Annotated

from fastapi import FastAPI, Query, Response

import meteogram
from meteogram.constants import config
from meteogram.schemas import Location

app = FastAPI(docs_url="/")
app.title = "Meteogram"


class QueryParams(Location):
    """Query parameters."""

    hours: int = config.HOURS
    symbol_interval: int = config.SYMBOL_INTERVAL
    locale: str = config.LOCALE
    timezone: str = config.TIMEZONE
    bgcolor: tuple[float, float, float] = config.BGCOLOR
    size_x: int = config.HORIZONTAL_SIZE
    size_y: int = config.VERTICAL_SIZE
    dpi: int = config.DPI


@app.get(
    "/meteogram",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
def get_meteogram(query: Annotated[QueryParams, Query()]) -> Response:
    """Return a meteogram as a png-image.

    Parameters to be provided as query parameters (required parameters in bold):

    - **lat**: Latitude in degrees (North is positive, South is negative)
    - **lon**: Longitude in degrees (East is positive, West is negative)
    - altitude: Ground surface height above sea level in whole meters. Optional but
      recommended for precise temperature values. When missing the internal topography
      model is used for temperature correction, which is rather course and may be
      incorrect in hilly terrain.
    - hours: Number of hours to forecast
    - symbol_interval: Number of hours between each weather symbol
    - locale: Locale for date formatting
    - timezone: Timezone for date formatting
    - bgcolor: Background color as a tuple of floats
    - size_x: Horizontal size in pixels
    - size_y: Vertical size in pixels
    - dpi: Dots per inch (resolution) to use when rendering the image
    """
    location = Location.model_validate(query.model_dump())
    fig = meteogram.create_meteogram(
        location, **query.model_dump(exclude={"lat", "lon", "altitude", "dpi"})
    )

    # Save the Matplotlib figure to a PNG image in memory
    img = io.BytesIO()
    fig.savefig(img, format="png", dpi=query.dpi)
    img.seek(0)

    return Response(content=img.read(), media_type="image/png")
