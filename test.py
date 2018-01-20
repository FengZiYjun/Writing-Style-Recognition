"""
	Test File
	Test the trained model with target file in ./test/ folder
"""

import argparse
from main import read_file
from main import save_file
import extract_features as ef
import data_cleaning


parser = argparse.ArgumentParser(description = 'get features')
parser.add_argument('string', metavar='file', type=str, help='a string of txt file name')
filename = parser.parse_args().string

TEST = './test/'

text = read_file(TEST + filename)
text = data_cleaning.text_clean(text)

features = ef.feature_extraction(text)

save_file('./output/' + 'feat_' + filename, features)

save_file('./output/' + 'cleaned_' + filename, text)


# Change the "prime.txt" to indicate the java program
save_file('./output/prime.txt', filename[:-4] + ' ' + str(1))