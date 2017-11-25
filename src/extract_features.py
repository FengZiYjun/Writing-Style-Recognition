import jieba 
import jieba.posseg as pseg
import nltk



def lexical_diversity(text):
    return len(set(text)) / len(text)

def dict2string(dictionary):
	string = ""
	for key in dictionary:
		string = string + str(key) + " " + str(dictionary[key]) + '\n'
	return string


def feature_extraction(text):

	lines = text.split('\n')

	features_dict = {}

	# 分词，标记词性
	print('正在分词...')
	#new_text = ""
	cond_tuple_list = []
	for line in lines:
		# seg_list = jieba.cut(line, cut_all=False)
		# new_text = new_text + " ".join(seg_list) + '\n'
		result = pseg.cut(line)
		for word, tag in result:
			cond_tuple_list.append((tag, word))

	# 不同词性高频词
	print('正在收集高频词...')
	cfd = nltk.ConditionalFreqDist(cond_tuple_list)
	useful_tags = ['p', 'c', 'e', 'u', 'y', 'f', 'z', 'd', 'v', 'a', 'ad']
	#tags = cfd.conditions()
	for each_tag in useful_tags:
		#print(each_tag + ': ')
		res = cfd[each_tag].most_common(10)
		#print(res)
		features_dict[each_tag] = cfd[each_tag].most_common(10)


	# 词汇丰富度
	print('词汇丰富度')
	words = [word for tag, word in cond_tuple_list]
	print('total_lexical_diversity: ' + str(lexical_diversity(words)))
	features_dict['total_lexical_diversity'] = lexical_diversity(words)

	# 统计标点
	"""
	print('统计标点')
	puctuation = '，。：？！“”…；、'
	total_puctuation = 0.0
	for item in puctuation:
		tmp = words.count(item)
		#print(item + 'count: ' + str(tmp))
		total_puctuation += tmp
		features_dict[item] = tmp
	for key in puctuation:
		features_dict[key] = features_dict[key] / total_puctuation
	"""

	return dict2string(features_dict)

	