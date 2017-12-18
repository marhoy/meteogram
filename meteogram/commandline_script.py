import argparse

import meteogram


def main():
    parser = argparse.ArgumentParser(
        description='Create a meteogram for a given location.')
    parser.add_argument('-p', '--place', default='Norway/Oslo/Oslo/Godlia',
                        help='The yr.no place to generate meteogram for')
    parser.add_argument('-t', '--hours', type=int, default=18,
                        help='How many hours to forecast')
    parser.add_argument('-s', '--symbol-interval', type=int, default=3)
    parser.add_argument('-l', '--locale', default='en_US.UTF-8')
    parser.add_argument('-o', '--output-file', default='meteogram.png')
    arguments = parser.parse_args()

    fig = meteogram.meteogram(place=arguments.place, hours=arguments.hours,
                              symbol_interval=arguments.symbol_interval,
                              locale=arguments.locale)
    fig.savefig(arguments.output_file)


if __name__ == '__main__':
    main()
