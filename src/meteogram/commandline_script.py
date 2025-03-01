"""CLI script for generating meteograms."""

import argparse

from meteogram import config, create_meteogram
from meteogram.get_weather_data import get_hourly_forecast


def main() -> None:
    """Generate a meteogram from the command line."""
    # with open("config.yaml", 'r') as yamlfile:
    #     cfg = yaml.load(yamlfile)

    parser = argparse.ArgumentParser(
        description="Create a meteogram for a given location."
    )
    parser.add_argument(
        "-p",
        "--place",
        default=config.LOCATION,
        help="The yr.no place to generate meteogram for",
    )
    parser.add_argument(
        "-t",
        "--hours",
        type=int,
        default=config.HOURS,
        help="How many hours to forecast",
    )
    parser.add_argument(
        "-s",
        "--symbol-interval",
        type=int,
        default=config.SYMBOL_INTERVAL,
    )
    parser.add_argument(
        "-l",
        "--locale",
        default=config.LOCALE,
    )
    parser.add_argument(
        "-o",
        "--output-file",
        default="meteogram.png",
    )
    arguments = parser.parse_args()

    data = get_hourly_forecast(arguments.place)

    fig = create_meteogram(
        data=data,
        hours=arguments.hours,
        symbol_interval=arguments.symbol_interval,
        locale=arguments.locale,
    )
    fig.savefig(arguments.output_file, facecolor=config.BGCOLOR)


if __name__ == "__main__":
    main()
