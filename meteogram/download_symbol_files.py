import io
import os
import zipfile

import requests

from . import constants


def download_wind_arrows(download_dir=constants.WIND_SYMBOLS_DIR):
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir, exist_ok=True)
    else:
        return

    # Example URL:
    # http://fil.nrk.no/yr/grafikk/vindpiler/32/vindpil.0000.225.png
    base_url = 'http://fil.nrk.no/yr/grafikk/vindpiler/32/'

    wind_directions = range(0, 360, 5)
    wind_speeds = range(0, 1025, 25)

    # Loop over wind-directions and -speeds and download the corresponding symbol
    for direction in wind_directions:
        for speed in wind_speeds:
            filename = 'vindpil.{:04}.{:03}.png'.format(speed, direction)
            url = base_url + filename
            r = requests.get(url, allow_redirects=True)
            open(os.path.join(download_dir, filename), 'wb').write(r.content)

    # Additionally, download the vindstille symbol
    filename = 'vindstille.png'
    url = base_url + filename
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(download_dir, filename), 'wb').write(r.content)


def download_weather_symbols(download_dir=constants.WEATHER_SYMBOLS_DIR):
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir, exist_ok=True)
    else:
        return

    r = requests.get('https://github.com/YR/weather-symbols/raw/master/yr-weather-symbols.zip')

    with zipfile.ZipFile(io.BytesIO(r.content)) as zip_file:
        zip_file.extractall(path=download_dir)


if __name__ == '__main__':
    download_wind_arrows()
    download_weather_symbols()
