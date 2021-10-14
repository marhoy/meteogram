import datetime

import matplotlib.dates
import pandas as pd
import requests
from bs4 import BeautifulSoup

from . import constants


def _create_url(place=constants.DEFAULT_PLACE):
    url = "https://www.yr.no/place/" + place
    return url


def get_hourly_forecast(place=constants.DEFAULT_PLACE):
    # url = _create_url(place) + '/varsel_time_for_time.xml'
    # response = requests.get(url)
    url = "https://api.met.no/weatherapi/locationforecast/2.0/classic.xml?altitude=132&lat=59.909068&lon=10.8392416"
    headers = {
        "Accept": "application/xml",
        "User-Agent": "https://github.com/marhoy/meteogram",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    rows = []
    for time in soup.find_all("time"):
        time_from = pd.to_datetime(time["from"])
        time_to = pd.to_datetime(time["to"])

        if time_from == time_to:
            row = dict()
            row["temp"] = float(time.temperature["value"])
            row["wind_dir"] = float(time.winddirection["deg"])
            row["wind_speed"] = float(time.windspeed["mps"])
            row["pressure"] = float(time.pressure["value"])
        elif time_to - time_from == pd.Timedelta("1 hour"):
            row["from"] = time_from
            row["to"] = time_to
            row["symbol"] = time.symbol["code"]
            row["precip"] = float(time.precipitation["value"])
            row["precip_min"] = float(time.precipitation["minvalue"])
            row["precip_max"] = float(time.precipitation["maxvalue"])

            rows.append(row)

    df = pd.DataFrame(rows)

    # Change the data type of the different columns
    # df["from"] = pd.to_datetime(df["from"])
    # df["to"] = pd.to_datetime(df["to"])

    # Create new columns with dates that are Matplotlib-friendly
    df["from_mpl"] = matplotlib.dates.date2num(
        df["from"]
    )  # .astype(datetime.datetime))
    df["to_mpl"] = matplotlib.dates.date2num(df["to"])  # .astype(datetime.datetime))
    return df


def get_precip_now(place=constants.DEFAULT_PLACE):
    url = _create_url(place) + "/varsel_nu.xml"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    column_names = ["time", "precip"]
    df = pd.DataFrame(columns=column_names)

    for time in soup.forecast.find_all("time"):
        row = pd.DataFrame(
            [[time["from"], time.precipitation["value"]]], columns=column_names
        )
        df = df.append(row)
    df = df.reset_index(drop=True)

    return df
