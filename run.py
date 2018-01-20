import argparse
import main

parser = argparse.ArgumentParser(description = 'get writing features of writers.')
parser.add_argument('string', metavar='file', type=str, help='a string of txt file path')
args = parser.parse_args()

main.main(args.string)