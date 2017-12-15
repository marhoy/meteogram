import pandas as pd
import requests
from bs4 import BeautifulSoup

from . import constants


def get_hourly_forecast(url=constants.HOURLY_URL):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    column_names = ['from', 'to', 'symbol', 'temp', 'precip', 'wind_dir', 'wind_speed', 'pressure']
    df = pd.DataFrame(columns=column_names)

    for time in soup.tabular.find_all("time"):
        row = pd.DataFrame([[
            time['from'],
            time['to'],
            time.symbol['var'],
            time.temperature['value'],
            time.precipitation['value'],
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
    df['wind_dir'] = df['wind_dir'].astype(float)
    df['wind_speed'] = df['wind_speed'].astype(float)
    df['pressure'] = df['pressure'].astype(float)

    return df


def get_precip_now(url=constants.NOW_URL):
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
