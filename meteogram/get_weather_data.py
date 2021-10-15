import matplotlib.dates
import pandas as pd
import requests
from bs4 import BeautifulSoup

from . import constants
from .schemas import Location


def get_hourly_forecast(
    location: Location = constants.DEFAULT_LOCATION,
) -> pd.DataFrame:
    """Get data from the Yr API and return a DataFrame."""
    url = "https://api.met.no/weatherapi/locationforecast/2.0/complete"
    headers = {
        "User-Agent": "https://github.com/marhoy/meteogram",
    }
    response = requests.get(url, headers=headers, params=location.dict())
    data = response.json()

    rows = []
    for time in data["properties"]["timeseries"]:

        if not "next_1_hours" in time["data"].keys():
            # This data point does not have information about next 1 hour
            continue

        instant_details = time["data"]["instant"]["details"]
        next_1_hour_details = time["data"]["next_1_hours"]

        row = dict()
        row["from"] = (
            pd.to_datetime(time["time"]).tz_convert("Europe/Oslo").tz_localize(tz=None)
        )
        row["temp"] = float(instant_details["air_temperature"])
        row["wind_dir"] = float(instant_details["wind_from_direction"])
        row["wind_speed"] = float(instant_details["wind_speed"])
        row["pressure"] = float(instant_details["air_pressure_at_sea_level"])

        row["symbol"] = next_1_hour_details["summary"]["symbol_code"]
        row["precip"] = float(next_1_hour_details["details"]["precipitation_amount"])
        row["precip_min"] = float(
            next_1_hour_details["details"]["precipitation_amount_min"]
        )
        row["precip_max"] = float(
            next_1_hour_details["details"]["precipitation_amount_max"]
        )

        rows.append(row)

    df = pd.DataFrame(rows)

    # Create a new column with a Matplotlib-friendly datetime
    df["from_mpl"] = matplotlib.dates.date2num(df["from"])

    return df


# def get_precip_now(place=constants.DEFAULT_PLACE):
#     url = _create_url(place) + "/varsel_nu.xml"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "lxml")

#     column_names = ["time", "precip"]
#     df = pd.DataFrame(columns=column_names)

#     for time in soup.forecast.find_all("time"):
#         row = pd.DataFrame(
#             [[time["from"], time.precipitation["value"]]], columns=column_names
#         )
#         df = df.append(row)
#     df = df.reset_index(drop=True)

#     return df
