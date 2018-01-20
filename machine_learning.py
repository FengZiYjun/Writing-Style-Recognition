import os
from plot import extract_feat_num,extract_freq_tag_ratio, read_feat, read_depen
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import itertools
from compare import normalize
import argparse
from sklearn.externals import joblib


OUTPUT = './output/'


AUTHORS = ['鲁迅', '王小波', '周作人', '江南']

def dict2row(feat_dict, depen_dict):
	# 不考虑高频词
	tmp1 = extract_feat_num(feat_dict)[0]
	tmp2 = extract_freq_tag_ratio(feat_dict)
	tmp_dict = {**tmp1, **tmp2, **normalize(depen_dict)}
	#print(len(tmp1.values()), len(tmp2.values()))
	return list(tmp_dict.values())

def make_input(author, test_ratio=0.2):
	list_of_train = []
	list_of_test = []
	cnt = 0
	feat_dict = {}
	while True:
		filename = OUTPUT + 'feat_' + author + str(cnt) + '.txt'
		if os.path.exists(filename) is True:
			cnt += 1
		else:
			break
	print(str(cnt) + ' files collected.')
	test_num = int(np.floor(cnt * test_ratio))

	# load train files
	#print(str(cnt - test_num) + ' files for training.')
	for i in range(cnt - test_num):
		feat_file = OUTPUT + 'feat_' + author + str(i) + '.txt'
		depen_file = OUTPUT + 'depen_' + author + str(i) + '.txt'
		row = dict2row(feat_dict, read_depen(depen_file))
		list_of_train.append(row)

	# load test files
	#print(str(test_num) + ' files for testing.')
	for i in range(cnt - test_num, cnt):
		feat_file = OUTPUT + 'feat_' + author + str(i) + '.txt'
		depen_file = OUTPUT + 'depen_' + author + str(i) + '.txt'
		row = dict2row(feat_dict, read_depen(depen_file))
		list_of_test.append(row)

	return np.array(list_of_train), np.array(list_of_test)


def train(author_list):
	author_names = author_list
	X_train = 0
	Y_train = 0
	X_test = 0
	Y_test = 0
	for author in author_names:
		x, x_t = make_input(author)
		#print(x)
		y = np.repeat(author_names.index(author), x.shape[0]).transpose()
		y_t = np.repeat(author_names.index(author), x_t.shape[0]).transpose()
		if type(X_train) is int:
			X_train = x
			Y_train = y
			X_test = x_t
			Y_test = y_t
		elif len(x) is not 0:
			X_train = np.vstack((X_train, x))
			X_test = np.vstack((X_test, x_t))
			Y_train = np.concatenate([Y_train, y])
			Y_test = np.concatenate([Y_test, y_t])
		else:
			continue

	#print(X_train.shape, X_test.shape)
	#print(Y_train.shape, Y_test.shape)
	
	print('training model...')
	from sklearn.ensemble import RandomForestClassifier
	clf = RandomForestClassifier().fit(X_train, Y_train)
	print('done')

	from plot_tool import train_test
	train_test.test(clf.predict(X_test), Y_test, class_names=author_names)

	# save the model
	joblib.dump(clf, 'classifier.clf')


def classify(author):
	sample = np.array(dict2row(read_feat(OUTPUT + 'feat_' + author + '.txt'), 
					read_depen(OUTPUT + 'depen_' + author + '.txt'))).reshape((1, -1))
	clf = joblib.load('classifier.clf')
	pred = clf.predict(sample)

	return AUTHORS[pred[0]]

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'get authors')
	parser.add_argument('string', metavar='file', type=str, help='author names')
	authors = parser.parse_args().string
	author_list = authors.split(',')
	if len(author_list) != 1:
		train(author_list)
	else:
		print('prediction: ', classify(author_list[0]))