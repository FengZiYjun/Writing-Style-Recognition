import extract_features as ef
import data_cleaning

OUTPUT = './output/'
INPUT = './input/'

def read_file(filename):
	with open(filename, encoding='utf-8') as f:
		text = f.read()
	return text

def save_file(filename, string):
	print('saving ' + filename + '...')
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(string)
	print('done')

LINES_PER_FILE = 500
def split_text(text):
	lines = text.split('\n')
	total_lines = len(lines)
	total_split = total_lines // LINES_PER_FILE
	split_list = []
	for i in range(total_split):
		split_list.append('\n'.join(lines[i*LINES_PER_FILE : (i+1)*LINES_PER_FILE]))
	print('split done.')
	return  split_list

def main(filenames):
	# receive arguments from run.py

	#-------------------- Encoding ------------------------
	
	file_list = filenames.split(',')
	for filename in file_list:
		print('dealing with ' + INPUT + filename)

		text = read_file(INPUT + filename)
		cleaned_text = data_cleaning.text_clean(text)

		# 作为统计的度量，对整个文本抽取feature
		features = ef.feature_extraction(cleaned_text)
		
		# save as the whole long text
		save_file(OUTPUT + 'cleaned_' + filename, cleaned_text)
		save_file(OUTPUT + 'all_feat_' + filename, features)
		
		# text = read_file('./output/cleaned_' + filename)
		
		# return list of string
		file_list = split_text(cleaned_text)
		
		cnt = 0
		author = filename[:-4]
		for file_text in file_list:

			# 作为学习样本，对切割好的文本抽取featuress
			file_features = ef.feature_extraction(file_text)

			# save the cleaned split text
			save_file(OUTPUT + 'cleaned_' + author + str(cnt) + '.txt', file_text)
			# save the feature of a single split text
			save_file(OUTPUT + 'feat_' + author + str(cnt) + '.txt', file_features)
			cnt += 1

	# the whole cleaned text is 'cleaned_author.txt' ----- for java program
	# features of the whole text is 'all_feat_author.txt' ------ for statistic ploting
	# the split cleaned text is 'cleaned_authori.txt' ------- for java program (not done yet)
	# features of the split text is 'feat_authori.txt' ---- for machine learning

	# ----------------------  End -------------------------