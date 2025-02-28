"""Get weather data from Yr API."""

import pandas as pd
import requests_cache
from loguru import logger

from meteogram.schemas import Location

# Create a session-object with caching determined by the response headers
session = requests_cache.CachedSession("yr_cache", cache_control=True)


def get_hourly_forecast(location: Location) -> pd.DataFrame:
    """Get hourly forecast data from the Yr API as a DataFrame.

    Args:
        location: The location (lat, lon, and optionally altitude)

    Returns:
        pd.Dataframe: Hourly forecast data
    """
    # Get data from the YR API. The resulting response will be returned from cache if
    # the previous response hasn't expired yet.
    url = "https://api.met.no/weatherapi/locationforecast/2.0/complete"
    headers = {
        "User-Agent": "https://github.com/marhoy/meteogram",
    }
    response = session.get(url, headers=headers, params=location.dict())
    response.raise_for_status()
    data = response.json()

    # Log info about caching
    if response.from_cache:
        logger.debug(f"Returned a cached response. Expires at {response.expires} GMT")
    else:
        logger.debug(
            "Retreived new data from api.met.no. "
            f"Expires at {response.headers['Expires']}"
        )

    rows = []
    for time in data["properties"]["timeseries"]:
        if "next_1_hours" not in time["data"]:
            # This data point does not have information about next 1 hour
            continue

        instant_details = time["data"]["instant"]["details"]
        next_1_hour_details = time["data"]["next_1_hours"]

        row = {}
        row["from"] = pd.to_datetime(time["time"])
        row["temp"] = float(instant_details["air_temperature"])
        row["wind_dir"] = float(instant_details["wind_from_direction"])
        row["wind_speed"] = float(instant_details["wind_speed"])
        row["pressure"] = float(instant_details["air_pressure_at_sea_level"])

        row["symbol"] = next_1_hour_details["summary"]["symbol_code"]
        row["precip"] = float(next_1_hour_details["details"]["precipitation_amount"])
        row["precip_min"] = float(
            next_1_hour_details["details"].get("precipitation_amount_min", 0)
        )
        row["precip_max"] = float(
            next_1_hour_details["details"].get("precipitation_amount_max", 0)
        )

        rows.append(row)

    return pd.DataFrame(rows)
