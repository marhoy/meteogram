import io

import flask

import meteogram

app = flask.Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def create_meteogram():
    location = flask.request.args.get("location", meteogram.DEFAULT_LOCATION)
    hours = int(flask.request.args.get("hours", meteogram.DEFAULT_HOURS))
    symbol_interval = int(
        flask.request.args.get("symbol_interval", meteogram.DEFAULT_SYMBOL_INTERVAL)
    )
    locale = flask.request.args.get("locale", meteogram.DEFAULT_LOCALE)

    fig = meteogram.meteogram(
        location=location, hours=hours, symbol_interval=symbol_interval, locale=locale
    )
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return flask.send_file(img, mimetype="image/png", cache_timeout=10)


def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
