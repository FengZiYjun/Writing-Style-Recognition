import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from os import path
from pillow import Image

def pie(dictionary):
	labels = list(dictionary.keys())
	values = [dictionary[key] for key in labels]
	fig1, ax1 = plt.subplots()
	ax1.pie(values, labels=labels, autopct='%1.1f%%')
	ax1.axis('equal')
	plt.show()

def hist(dictionary):
	labels = tuple(dictionary.keys())
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
	plt.show()

def cloud(dictionary):
	text = " ".join([((key + ' ') * dictionary[key])  for key in list(dictionary.keys())])
	print(text)
	my_wordcloud = WordCloud().generate(text)
	plt.figure()
	plt.imshow(my_wordcloud, interpolation='bilinear')
	plt.axis('off')
	plt.show()

# to be tested
def freeCloud(dictionary):
	alice_mask = np.array(Image.open(path.join(d, "alice_mask.png")))
	wc = WordCloud(background_color="white", max_words=200, mask=alice_mask)
	wc.to_file(path.join(d, "alice.png"))
	plt.figure()
	plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
	plt.axis('off')
	plt.show()
	


def test():
	cloud({'ab':12, 'bd':32, 'cr':11})
	

test()