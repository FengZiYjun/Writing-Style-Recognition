import re
import visualize as vs

PATH = './output/'


def makeTupleList(string):
	pattern = r'\(.*?\)'
	find_list = re.findall(pattern, string)
	ret = list()
	for item in find_list:
		split_list = item[2:-1].split(', ')
		ret.append((split_list[0][:-1], int(split_list[1])))
	return ret


# re-fetch the data from txt files
# return a dictionary
def read_feat(filename):
	with open(filename, encoding='utf-8') as f:
		lines = f.read().split('\n')
	ret = dict()
	for line in lines:
		if line == "":
			continue
		try:
			i = line.index('[')
			if i - 1 >= 1:
				key = line[:i]
				value = line[i:]
			value = makeTupleList(value)
		except:
			key = line.split(' ')[0]
			value = line.split(' ')[1]
			value = float(value)
		ret[key] = value
		#print(key, value)
	return ret


def read_depen(filename):
	with open(filename, encoding='utf-8') as f:
		lines = f.read().split('\n')
	ret = dict()
	for line in lines:
		if line=="":
			continue
		tmp = line.split(' ')
		ret[tmp[0]] = float(tmp[1])
	return ret


def merge(feat_dict, depen_dict):
	return {**feat_dict, **depen_dict}


def score_list(list1, list2):
	weights = [1, 0.8, 0.5, 0.3, 0.1]
	error = 0.0
	up_bound = min(len(list1), len(list2), len(weights))
	sum_list1 = sum([value for (key, value) in list1[:up_bound]])
	sum_list2 = sum([value for (key, value) in list2[:up_bound]])
	i = 0
	while(i < up_bound):
		if list1[i][0] == list2[i][0]:
			error += weights[i] * abs(list1[i][1] / sum_list1 - list2[i][1] / sum_list2)
		else:
			error +=  1
		i += 1
	return error


def score_float(f1, f2):
	return abs(f1 - f2)


def compare(dict1, dict2):
	keys = set(dict1.keys()).intersection(set(dict2.keys()))
	score = 0.0
	for key in keys:
		add_score = 0.0
		if type(dict1[key]) == list:
			add_score += score_list(dict1[key], dict2[key])
		else:
			add_score += score_float(dict1[key], dict2[key])
		#print(key + ': ' + str(add_score))
		score += add_score
	return score


#feat = read_feat(PATH + 'feat_liucixin.txt')
#print(feat)
#feat2 = read_depen(PATH + 'depen_liucixin.txt')
#print(feat2)
#print(compare(feat2, feat2))

def main(args):
	filename1 = args[0] + '.txt'
	filename2 = args[1] + '.txt'
	print('comparing ' + args[0] + ' and ' + args[1])
	feature_dict1 = merge(read_feat(PATH + 'feat_' + filename1), read_depen(PATH + 'depen_' + filename1))
	feature_dict2 = merge(read_feat(PATH + 'feat_' + filename2), read_depen(PATH + 'depen_' + filename2))
	print('total score: ')
	print(compare(feature_dict1, feature_dict2))
