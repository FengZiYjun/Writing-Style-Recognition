import extract_features as ef
import data_cleaning

OUTPUT = './output/'
INPUT = './input/'

def read_file(filename):
	#PATH = "D:\\Courses\\NLP\\LAB\\Corpus\\鲁迅全集\\"
	#FILENAME = 'luxunquanji.txt'
	with open(filename, encoding='utf-8') as f:
		text = f.read()
	return text

def save_file(filename, string):
	print('saving...')
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(string)
	print('done')


def main(filenames):

	file_list = filenames.split(',')
	for filename in file_list:
		print('dealing with ' + INPUT + filename)

		text = read_file(INPUT + filename)
		cleaned_text = data_cleaning.text_clean(text)
		features = ef.feature_extraction(cleaned_text)
		
		save_file(OUTPUT + 'cleaned_' + filename, cleaned_text)
		save_file(OUTPUT + 'feat_' + filename, features)
	
