#coding:utf-8
import re
#import visualize as vs
import excel

PATH = './output/'
INPUT = './input/'

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


def author_info():
	for author, chin_name in zip(author_names, chin_names):
		au_dict = read_depen(PATH + 'depen_' + author + '.txt')
		vs.pie(au_dict, chin_name)


# ---------------------- Feature Extractor ---------------------


def extract_tag_word(dictionary):
	# 抽取高频功能词列表
	useful_tags = ['p', 'c', 'e', 'u', 'y', 'f', 'z', 'd', 'v', 'a', 'ad']
	return {tag:dictionary[tag] for tag in useful_tags}

def extract_freq_tag_ratio(dictionary):
	# 抽取高频功能词的比例
	tmp = {key[1:]:dictionary[key] for key in dictionary if key[0] is '%'}
	useful_tags = ['p', 'c', 'e', 'u', 'y', 'f', 'z', 'd', 'v', 'a', 'ad']
	return {item: tmp.get(item, 0) for item in useful_tags}


def extract_tag_ratio(dictionary):
	# 抽取词性比例数据
	tmp = {key[1:]:dictionary[key] for key in dictionary if key[0] is '%'}
	new_dict = {}
	for item in tmp:
		# 只选取词性的大类
		tag = tag_mapping[item[0]]
		if tag in list(new_dict.keys()):
			new_dict[tag] = new_dict[tag] + tmp[item]
		else:
			new_dict[tag] = tmp[item]
	return new_dict


def extract_feat_num(dictionary):
	# 抽取其他特征数据
	mapping = {'question':'疑问句比例','emotion':'感叹句比例','mean_sent_length':'平均句长','short_ratio':'短句比例','long_ratio':'长句比例',
	'total_lexical_diversity':'词汇丰富度','once':'单现词比例'}	
	#ret =  {mapping[key]:dictionary[key] for key in dictionary if type(dictionary[key]) is not list and key[0] is not '%'}
	ret = {mapping[key]: dictionary.get(key, 0) for key in mapping}
	return ret, ret.keys()

# --------------------------------- End -------------------------------

# -------------------------- Drawing Functions --------------------

def draw_tag_ratio():
	data = []
	for author, chin_name in zip(author_names, chin_names):
		au_dict = read_feat(PATH + 'all_feat_' + author + '.txt')
		au_dict = extract_tag_ratio(au_dict)
		excel.save_dict(au_dict, chin_name+'作品词性比例')
		vs.pie(au_dict, chin_name, '作品词性比例')
		data.append([au_dict.get(key, 0) for key in list(tag_mapping.values())])
	excel.save_table(data, list(tag_mapping.values()), chin_names, '词性比例总表')


def draw_feat_table():
	data = []
	colLabels = []
	for author in author_names:
		au_dict = read_feat(PATH + 'all_feat_' + author + '.txt')
		au_dict, colLabels = extract_feat_num(au_dict)
		data.append(list(au_dict.values()))
	excel.save_table(data, list(colLabels), chin_names, '特征统计表')

def make_word_cloud():
	# 抽取高频词数据
	for author, chin_name in zip(author_names, chin_names):
		au_dict = read_feat(PATH + 'all_feat_' + author + '.txt')
		# extract the frequency list & mapping into chinese keys
		au_dict = {tag_mapping[key]:au_dict[key] for key in list(au_dict.keys()) if type(au_dict[key]) is list}
		for key in au_dict.keys():
			if len(au_dict[key]) != 0:
				vs.cloud({item[0]:item[1] for item in au_dict[key]}, chin_name, '作品' + key + '词云')

def draw_depen_table():
	data = []
	for author in author_names:
		au_dict = read_depen(PATH + 'depen_' + author + '.txt')
		data.append(list(au_dict.values()))
		#print(au_dict)
	excel.save_table(data, list(au_dict.keys()), chin_names, '句法依存标注统计表')

# ------------------------------ End -----------------------------------


# -------------- main control -------------------

def plot_main(filenames):
	file_list = filenames.split(',')
	global author_names
	author_names = [file[:-4] for file in file_list]

	# if chinese author names provided
#	global chin_names
#	chin_names = author_names


	author_info()
	draw_tag_ratio()
	draw_feat_table()
	make_word_cloud()
	draw_depen_table()

