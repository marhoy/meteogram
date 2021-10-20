"""Get weather data from Yr API."""

from typing import Optional

import matplotlib.dates
import pandas as pd
import requests

from meteogram import config
from meteogram.schemas import Location


def get_hourly_forecast(location: Optional[Location] = None) -> pd.DataFrame:
    """Get data from the Yr API and return a DataFrame."""
    if location is None:
        location = config.LOCATION

    url = "https://api.met.no/weatherapi/locationforecast/2.0/complete"
    headers = {
        "User-Agent": "https://github.com/marhoy/meteogram",
    }
    response = requests.get(url, headers=headers, params=location.dict())
    response.raise_for_status()
    data = response.json()

    rows = []
    for time in data["properties"]["timeseries"]:

        if "next_1_hours" not in time["data"].keys():
            # This data point does not have information about next 1 hour
            continue

        instant_details = time["data"]["instant"]["details"]
        next_1_hour_details = time["data"]["next_1_hours"]

        row = dict()
        row["from"] = (
            pd.to_datetime(time["time"])
            .tz_convert(config.TIMEZONE)
            .tz_localize(tz=None)
        )
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

    df = pd.DataFrame(rows)

    # Create a new column with a Matplotlib-friendly datetime
    df["from_mpl"] = matplotlib.dates.date2num(df["from"])

    return df
