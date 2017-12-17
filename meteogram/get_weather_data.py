import datetime

import matplotlib.dates
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from . import constants


def _create_url(place=constants.DEFAULT_PLACE):
    url = 'https://www.yr.no/place/' + place
    return url


def get_hourly_forecast(place=constants.DEFAULT_PLACE):

    url = _create_url(place) + '/varsel_time_for_time.xml'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    column_names = ['from', 'to', 'symbol', 'temp', 'precip', 'precip_min', 'precip_max', 'wind_dir', 'wind_speed', 'pressure']
    df = pd.DataFrame(columns=column_names)

    for time in soup.tabular.find_all("time"):
        row = pd.DataFrame([[
            time['from'],
            time['to'],
            time.symbol['var'],
            time.temperature['value'],
            time.precipitation['value'],
            time.precipitation.get('minvalue', 0),
            time.precipitation.get('maxvalue', 0),
            time.winddirection['deg'],
            time.windspeed['mps'],
            time.pressure['value']
        ]], columns=column_names)
        df = df.append(row)
    df = df.reset_index(drop=True)

    # Change the data type of the different columns
    df['from'] = pd.to_datetime(df['from'])
    df['to'] = pd.to_datetime(df['to'])
    df['temp'] = df['temp'].astype(int)
    df['precip'] = df['precip'].astype(float)
    df['precip_min'] = df['precip_min'].astype(float)
    df['precip_max'] = df['precip_max'].astype(float)
    df['wind_dir'] = df['wind_dir'].astype(float)
    df['wind_speed'] = df['wind_speed'].astype(float)
    df['pressure'] = df['pressure'].astype(float)

    # Create new columns with dates that are Matplotlib-friendly
    df['from_mpl'] = matplotlib.dates.date2num(df['from'].astype(datetime.datetime))
    df['to_mpl'] = matplotlib.dates.date2num(df['to'].astype(datetime.datetime))
    return df


def get_precip_now(place=constants.DEFAULT_PLACE):

    url = _create_url(place) + '/varsel_nu.xml'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    column_names = ['time', 'precip']
    df = pd.DataFrame(columns=column_names)

    for time in soup.forecast.find_all("time"):
        row = pd.DataFrame([[
            time['from'],
            time.precipitation['value']
        ]], columns=column_names)
        df = df.append(row)
    df = df.reset_index(drop=True)

    return df
