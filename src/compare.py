#coding:utf-8
import re
import visualize as vs
import excel
from scipy.spatial import distance

PATH = './output/'

author_names = ['luxun', 'zhouzuoren', 'linyutang', 'sanmao', 'wangxiaobo',
	'liucixin', 'shitiesheng']
chin_names = ['鲁迅', '周作人', '林语堂', '三毛','王小波','刘慈欣','史铁生']

tag_mapping = {'a':'形容词','ad':'副形词','ag':'形容词性语素','an':'名形词',
	'b':'区别词',
	'c':'连词',
	'd':'副词', 'df':'副词','dg':'副语素',
	'e':'叹词',
	'eng':'外语',
	'f':'方位词',
	'g':'语素',
	'h':'前接成分',
	'i':'成语',
	'j':'简称略语',
	'k':'后接成分',
	'l':'习用语',
	'm':'数词', 'mg':'数语素','mq':'数词',
	'n':'名词', 'ns':'地名', 'nr':'人名', 'nt':'机构名','nz':'其他专名','ng':'名语素','nrfg':'名词','nrt':'名词',
	'o':'拟声词',
	'p':'介词',
	'q':'量词',
	'r':'代词',
	's':'处所词',
	't':'时间词', 'tg':'时间素',
	'u':'助词','uj':'助词','ug':'助词','ud':'助词','ul':'助词','uv':'助词','uz':'助词',
	'v':'动词', 'vn':'名动词','vd':'副动词','vg':'动语素','vq':'动词',
	'w':'标点符号',
	'x':'非语素字','y':'语气词',
	'z':'状态词','zg':'状态词'
	}


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
				key = line[:i-1]
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

def author_info():
	for author, chin_name in zip(author_names, chin_names):
		au_dict = read_depen(PATH + 'depen_' + author + '.txt')
		vs.pie(au_dict, chin_name)

def extract_tag_word(dictionary):
	useful_tags = ['p', 'c', 'e', 'u', 'y', 'f', 'z', 'd', 'v', 'a', 'ad']
	return {tag:dictionary[tag] for tag in useful_tags}


def extract_tag_ratio(dictionary):
	tmp = {key[1:]:dictionary[key] for key in dictionary if key[0] is '%'}
	
	new_dict = {}
	for item in tmp:
		tag = tag_mapping[item[0]]
		if tag in list(new_dict.keys()):
			new_dict[tag] = new_dict[tag] + tmp[item]
		else:
			new_dict[tag] = tmp[item]
	return new_dict

def extract_feat_num(dictionary):
	mapping = {'question':'疑问句比例','emotion':'感叹句比例','mean_sent_length':'平均句长','short_ratio':'短句比例','long_ratio':'长句比例',
	'total_lexical_diversity':'词汇丰富度','once':'单现词比例'}	
	ret =  {mapping[key]:dictionary[key] for key in dictionary if type(dictionary[key]) is not list and key[0] is not '%'}
	
	return ret, ret.keys()

def draw_tag_ratio():
	data = []
	for author, chin_name in zip(author_names, chin_names):
		au_dict = read_feat(PATH + 'feat_' + author + '.txt')
		au_dict = extract_tag_ratio(au_dict)
		#excel.save_dict(au_dict, chin_name+'作品词性比例')
		#vs.pie(au_dict, chin_name, '作品词性比例')
		data.append([au_dict.get(key, 0) for key in list(tag_mapping.values())])
	excel.save_table(data, list(tag_mapping.values()), chin_names, '词性比例总表')

def draw_table():
	data = []
	colLabels = []
	for author, chin_name in zip(author_names, chin_names):
		au_dict = read_feat(PATH + 'feat_' + author + '.txt')
		au_dict, colLabels = extract_feat_num(au_dict)
		data.append(list(au_dict.values()))
		#print(au_dict)
	excel.save_table(data, list(colLabels), chin_names, '特征统计表')

def make_word_cloud():
	author_names = ['shitiesheng']
	chin_names = ['史铁生']
	for author, chin_name in zip(author_names, chin_names):
		au_dict = read_feat(PATH + 'feat_' + author + '.txt')
		# extract the frequency list & mapping into chinese keys
		au_dict = {tag_mapping[key]:au_dict[key] for key in list(au_dict.keys()) if type(au_dict[key]) is list}
		for key in au_dict.keys():
			if len(au_dict[key]) != 0:
				vs.cloud({item[0]:item[1] for item in au_dict[key]}, chin_name, '作品' + key + '词云')

def draw_depen_table():
	data = []
	for author, chin_name in zip(author_names, chin_names):
		au_dict = read_depen(PATH + 'depen_' + author + '.txt')
		data.append(list(au_dict.values()))
		#print(au_dict)
	excel.save_table(data, list(au_dict.keys()), chin_names, '句法依存标注统计表')


def main(args):
	#filename1 = args[0] + '.txt'
	#filename2 = args[1] + '.txt'

	#author_info()
	#draw_tag_ratio()
	#draw_table()
	#make_word_cloud()
	draw_depen_table()

main(0)