import plot
import os
import numpy as np
OUTPUT = './output/'



def dict2row(dictionary):
	# 不考虑高频词
	tmp_dict = (plot.extract_feat_num(dictionary)[0]).update(extract_tag_ratio(dictionary))
	return list(tmp_dict.values())

def make_input(author):
	list_of_list = []
	num = 0
	feat_dict = {}
	while True:
		filename = OUTPUT + 'feat_' + author + str(num) + '.txt'
		num += 1
		if os.path.exists(filename) is True:
			feat_dict = plot.read_feat(filename)
			row = dict2row(feat_dict)
			list_of_list.append(row)
		else:
			break
	return np.array(list_of_list)


def main():
	author_names = ['luxun', 'zhouzuoren', 'linyutang', 'sanmao', 'wangxiaobo',
	'liucixin', 'shitiesheng']
	X = np.array()
	Y = np.array()
	for author in author_names:
		x = make_input(author)
		y = np.repeat(author_names.index(author), x.shape[0]).transpose()
		np.vstack((X, x))
		np.vstack((Y, y))