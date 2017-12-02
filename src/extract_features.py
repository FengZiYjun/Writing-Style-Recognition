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
	
	features_dict = {}
	lines = text.split('\n')

	line_length = []
	ques_sent = 0
	emot_sent = 0
	
	# 分词，标记词性
	print('正在分词...')
	#new_text = ""
	cond_tuple_list = []
	for line in lines:
		if line=="\n" or len(line)==0:
			continue
		line_length.append(len(line))
		if line[-1] == "？":
			ques_sent += 1
		elif line[-1] == "！":
			emot_sent += 1

		result = pseg.cut(line)
		for word, tag in result:
			cond_tuple_list.append((tag, word))

	print('疑问句和感叹句...')
	features_dict['question'] = ques_sent / len(line_length)
	features_dict['emotion'] = emot_sent / len(line_length)

	print('计算句长...')
	mean_length = sum(line_length) / len(line_length)
	features_dict['mean_sent_length'] = mean_length
	
	print('计算长短句...')
	print(features_dict['mean_sent_length'])
	len_fdist = nltk.FreqDist(line_length)
	long_setense = 0
	short_sentense = 0
	for length in len_fdist:
		if length > 2 * mean_length:
			long_setense += len_fdist[length]
		if length < 0.5 * mean_length:
			short_sentense += len_fdist[length]
	features_dict['long_ratio'] = long_setense / len_fdist.N()
	features_dict['short_ratio'] = short_sentense / len_fdist.N()


	# 词性比例
	print('正在计算词性比例...')
	cfd = nltk.ConditionalFreqDist(cond_tuple_list)
	total_words = cfd.N()
	for tag in cfd.conditions():
		features_dict['%' + tag] = sum(cnt for word, cnt in cfd[tag].most_common()) / total_words


	# 高频虚词
	print('正在收集高频虚词...')
	useful_tags = ['p', 'c', 'e', 'u', 'y', 'f', 'z', 'd', 'v', 'a', 'ad']
	for each_tag in useful_tags:
		features_dict[each_tag] = cfd[each_tag].most_common(10)


	# 词汇丰富度
	print('词汇丰富度')
	words = [word for tag, word in cond_tuple_list]
	print('total_lexical_diversity: ' + str(lexical_diversity(words)))
	features_dict['total_lexical_diversity'] = lexical_diversity(words)


	# 单现词比例
	print('计算单现词比例...')
	fdist = nltk.FreqDist(words)
	features_dict['once'] = list(fdist.values()).count(1) / len(fdist.values())

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

	