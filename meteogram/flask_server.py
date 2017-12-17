import io

import flask

from meteogram import make_meteogram, constants

app = flask.Flask(__name__)


@app.route('/meteogram', methods=['POST', 'GET'])
def create_meteogram():
    place = flask.request.args.get('place', constants.DEFAULT_PLACE)
    hours = int(flask.request.args.get('hours', constants.DEFAULT_HOURS))
    symbol_interval = int(flask.request.args.get('symbol_interval', constants.DEFAULT_SYMBOL_INTERVAL))
    locale = flask.request.args.get('locale', constants.DEFAULT_LOCALE)

    fig = make_meteogram.meteogram(place=place, hours=hours, symbol_interval=symbol_interval, locale=locale)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return flask.send_file(img, mimetype='image/png', cache_timeout=10)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
