import compare
import argparse

parser = argparse.ArgumentParser(description = 'compare the style of two authors')
parser.add_argument('author1', metavar='file', type=str, help='the name of the first author')
parser.add_argument('author2', metavar='file', type=str, help='the name of the second author')
args = parser.parse_args()

compare.main([args.author1, args.author2])