#coding:utf-8
#
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import numpy as np
from wordcloud import WordCloud
#from os import path
#from pillow import Image

PATH = './output/'

def table(data, colLabels, rowLabels, title):
	# data ---- 2-D list
	fig, ax = plt.subplots()
	colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rowLabels)))
	ax.table(cellText = data, rowLabels=rowLabels, colLabels=colLabels,
			rowColours=colors, loc='center')
	plt.title( u'' + title)
	fig.tight_layout()
	plt.savefig(PATH  + title + '.jpg')
	print('matplotlib figure saved: '  + title + '.jpg')


def pie(dictionary, name, title):
	labels = list(dictionary.keys())
	# Chinese special encoding for matplotlib
	labels = [u'' + key for key in labels]
	values = [dictionary[key] for key in labels]
	total = sum(values)
	for x in range(len(labels)):
		if dictionary[labels[x]] < total * 0.005:
			labels[x] = u''
	fig1, ax1 = plt.subplots()
	colors = ['yellowgreen','red','gold','lightskyblue','lightcoral','pink', 'darkgreen','yellow','grey','violet','magenta','cyan']
	ax1.pie(values, labels=labels, colors = colors, autopct='%1.1f%%')
	ax1.axis('equal')
	plt.title(name + u'' + title)
	plt.savefig(PATH + name + title + '.jpg')
	print('matplotlib figure saved: ' + name + title + '.jpg')


def hist(dictionary, name, title):
	labels = tuple(dictionary.keys())
	print(labels)
	values = [dictionary[key] for key in labels]
	plt.rcdefaults()
	fig, ax = plt.subplots()
	y_pos = np.arange(len(labels))
	performance = values
	ax.barh(y_pos, performance, align='center',
	        color='green', ecolor='black')
	ax.set_yticks(y_pos)
	ax.set_yticklabels(labels)
	ax.invert_yaxis()  # labels read top-to-bottom
	ax.set_xlabel('values')
	ax.set_title('Key-Values')
	#plt.show()
	plt.title(name + u'' + title)
	plt.savefig(PATH + name + title + '.jpg')


def cloud(dictionary, name, title):
	if dictionary is None:
		print('Empty dictionary!')
		return
	font = r'C:\Windows\Fonts\simfang.ttf'
	my_wordcloud = WordCloud(background_color="white",collocations=False, font_path=font).generate_from_frequencies(dictionary)
	plt.figure()
	plt.imshow(my_wordcloud, interpolation='bilinear')
	plt.axis('off')
	plt.title(name + u'' + title)
	plt.savefig(PATH + name + title + '.jpg')
	plt.close()
	print('matplotlib figure saved: ' + name + title + '.jpg')

"""
# to be tested
def freeCloud(dictionary):
	alice_mask = np.array(Image.open(path.join(d, "alice_mask.png")))
	wc = WordCloud(background_color="white", max_words=200, mask=alice_mask)
	wc.to_file(path.join(d, "alice.png"))
	plt.figure()
	plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
	plt.axis('off')
	plt.show()
	
"""
"""
def test():
	cloud({'ab':12, 'bd':32, 'cr':11})
	

test()

"""
"""
text = {'在':43, '哈':34}
font = r'C:/Windows/Fonts/simsun.ttc'
my_wordcloud = WordCloud(background_color="white", font_path=font, stopwords=set('hey'), random_state=42, collocations=False, normalize_plurals=False).generate_from_frequencies(text)
plt.figure()
plt.imshow(my_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
"""