from plot import extract_feat_num,extract_freq_tag_ratio, read_feat
import os
import numpy as np
OUTPUT = './output/'


def dict2row(dictionary):
	# 不考虑高频词
	tmp1 = extract_feat_num(dictionary)[0]
	tmp2 = extract_freq_tag_ratio(dictionary)
	tmp_dict = {**tmp1, **tmp2}
	#print(len(tmp1.values()), len(tmp2.values()))
	return list(tmp_dict.values())

def make_input(author):
	list_of_list = []
	num = 2
	feat_dict = {}
	while True:
		filename = OUTPUT + 'feat_' + author + str(num) + '.txt'
		num += 1
		if os.path.exists(filename) is True:
			feat_dict = read_feat(filename)
			row = dict2row(feat_dict)
			list_of_list.append(row)
		else:
			break
	return np.array(list_of_list)


def main():
	author_names = ['luxun', 'zhouzuoren', 'linyutang', 'sanmao', 'wangxiaobo','liucixin', 'shitiesheng']
	X = 0
	Y = 0
	for author in author_names:
		x = make_input(author)
		#print(x)
		y = np.repeat(author_names.index(author), x.shape[0]).transpose()
		if type(X) is int:
			X = x
			Y = y
		elif len(x) is not 0:
			X = np.vstack((X, x))
			Y = np.vstack((Y, y))
		else:
			continue

	print(X.shape)
	# model.fit(X, Y)




main()