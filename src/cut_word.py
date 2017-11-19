import jieba 
import jieba.posseg as pseg
import nltk
import data_cleaning

def lexical_diversity(text):
    return len(set(text)) / len(text)

PATH = "D:\\Courses\\NLP\\LAB\\Corpus\\鲁迅全集"

with open(PATH + 'luxunquani.txt', encoding='utf-8') as f:
	text = f.read()

text = data_cleaning.text_clean(text)

lines = text.split('\n')

features_dict = {}

# 分词，标记词性
#new_text = ""
cond_tuple_list = []
for line in lines:
	# seg_list = jieba.cut(line, cut_all=False)
	# new_text = new_text + " ".join(seg_list) + '\n'
	result = pseg.cut(line)
	for word, tag in result:
		cond_tuple_list.append((tag, word))

# 不同词性高频词
cfd = nltk.ConditionalFreqDist(cond_tuple_list)
tags = cfd.conditions()
for each_tag in tags:
	print(each_tag + ': ')
	res = cfd[each_tag].most_common(10)
	print(res)
	features_dict[each_tag] = cfd[each_tag].most_common(10)


# 词汇丰富度
words = [word for tag, word in cond_tuple_list]
print('total lexical_diversity: ' + str(lexical_diversity(words)))
features_dict['total lexical_diversity'] = lexical_diversity(words)

# 统计标点
puctuation = '，。：？！“”…；、'
for item in puctuation:
	tmp = words.count(item)
	print(item + 'count: ' + str(tmp))
	features_dict[item] = tmp

with open('quanji_features.txt', 'w',encoding='utf-8') as f:
	f.write(str(features_dict))
