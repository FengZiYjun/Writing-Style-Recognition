import extract_features as ef
import data_cleaning

OUTPUT = './output/'
INPUT = './input/'

def read_file(filename):
	with open(filename, encoding='utf-8') as f:
		text = f.read()
	return text

def save_file(filename, string):
	print('saving...')
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(string)
	print('done')

LINES_PER_FILE = 500
def split_text(text, author):
	lines = text.split('\n')
	total_lines = len(lines)
	total_split = total_lines // LINES_PER_FILE
	for i in range(total_split):
		save_file(OUTPUT + author + str(i) + '.txt', '\n'.join(lines[i*LINES_PER_FILE : (i+1)*LINES_PER_FILE]))
	print('split done.')

def main(filenames):

	file_list = filenames.split(',')
	for filename in file_list:
		print('dealing with ' + INPUT + filename)

		text = read_file(INPUT + filename)
		cleaned_text = data_cleaning.text_clean(text)
		features = ef.feature_extraction(cleaned_text)
		
		save_file(OUTPUT + 'cleaned_' + filename, cleaned_text)
		save_file(OUTPUT + 'feat_' + filename, features)
		
		#text = read_file('./output/cleaned_' + filename)
		text = cleaned_text
		split_text(text, filename[:-4])
		# generate files named (author + number + .txt)