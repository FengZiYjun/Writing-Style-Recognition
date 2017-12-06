
def score_freq_word_list(list1, list2):
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


def normalize(dictionary):
	total = sum(dictionary.values())
	for key in list(dictionary.keys()):
		dictionary[key] = dictionary[key] / total
	return dictionary

def compute_distance(vec1, vec2):
	return distance.cosine(vec1, vec2)

def compare_depen(dict1, dict2):
	score = 0.0
	dict1 = normalize(dict1)
	dict2 = normalize(dict2)
	add_list = []
	score = compute_distance(list(dict1.values()), list(dict2.values()))
	return score, add_list

def compare_two_authors(author1, author2):
	print('comparing ' + author1 + ' and ' + author2)
	feature_dict1 = read_depen(PATH + 'depen_' + author1 + '.txt')
	feature_dict2 = read_depen(PATH + 'depen_' + author2 + '.txt')
	score, add_list = compare_depen(feature_dict1, feature_dict2)
	add_list = sorted(add_list, key=lambda i:i[1] ,reverse=True)
	return score
