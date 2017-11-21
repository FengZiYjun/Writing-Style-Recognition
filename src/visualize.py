import matplotlib.pyplot as plt

def pie(dictionary):
	labels = list(dictionary.keys())
	values = [dictionary[key] for key in labels]
	fig1, ax1 = plt.subplots()
	ax1.pie(values, labels=labels, autopct='%1.1f%%')
	ax1.axis('equal')
	plt.show()

def hist(dictionary):
	pass

def cloud(dictionary):
	pass

def test():
	pie({'a':12, 'b':32, 'c':11})

test()