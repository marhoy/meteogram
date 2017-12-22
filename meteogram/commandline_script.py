import argparse

import meteogram
import yaml


def main():

    # with open("config.yaml", 'r') as yamlfile:
    #     cfg = yaml.load(yamlfile)

    parser = argparse.ArgumentParser(
        description='Create a meteogram for a given location.')
    parser.add_argument('-p', '--place', default=meteogram.DEFAULT_PLACE,
                        help='The yr.no place to generate meteogram for')
    parser.add_argument('-t', '--hours', type=int, default=meteogram.DEFAULT_HOURS,
                        help='How many hours to forecast')
    parser.add_argument('-s', '--symbol-interval', type=int, default=meteogram.DEFAULT_SYMBOL_INTERVAL)
    parser.add_argument('-l', '--locale', default=meteogram.DEFAULT_LOCALE)
    parser.add_argument('-o', '--output-file', default='meteogram.png')
    arguments = parser.parse_args()

    fig = meteogram.meteogram(place=arguments.place, hours=arguments.hours,
                              symbol_interval=arguments.symbol_interval,
                              locale=arguments.locale)
    fig.savefig(arguments.output_file, facecolor=meteogram.DEFAULT_BGCOLOR)


if __name__ == '__main__':
    main()
