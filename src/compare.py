import re

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
		print(key, value)
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
	keys = list(dict1.keys())
	score = 0.0
	for key in keys:
		if type(key) == list:
			score += score_list(dict1[key], dict2[key])
		else:
			score += score_float(dict1[key], dict2[key])
	return score


#feat = read_feat(PATH + 'feat_liucixin.txt')
#print(feat)
#feat2 = read_depen(PATH + 'depen_liucixin.txt')
#print(feat2)
#print(compare(feat2, feat2))

def main():
	filename1 = 
	filename2 = 
	feature_dict1 = merge(read_feat(filename1), read_depen(filename1))
	feature_dict2 = merge(read_feat(filename2), read_depen(filename2))
	compare(feature_dict1, feature_dict2)