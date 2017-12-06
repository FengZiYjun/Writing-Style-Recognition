import plot
import argparse

parser = argparse.ArgumentParser(description = 'compare the style of two authors')
parser.add_argument('authors', metavar='file', type=str, help='the name of the authors')
args = parser.parse_args()

plot.plot_main(args.authors)