import os
from plot import extract_feat_num,extract_freq_tag_ratio, read_feat, read_depen
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import itertools
from compare import normalize
OUTPUT = './output/'


def dict2row(feat_dict, depen_dict):
	# 不考虑高频词
	tmp1 = extract_feat_num(feat_dict)[0]
	tmp2 = extract_freq_tag_ratio(feat_dict)
	tmp_dict = {**tmp1, **tmp2, **normalize(depen_dict)}
	#print(len(tmp1.values()), len(tmp2.values()))
	return list(tmp_dict.values())

def make_input(author):
	list_of_train = []
	list_of_test = []
	cnt = 0
	feat_dict = {}
	while True:
		filename = OUTPUT + 'feat_' + author + str(cnt) + '.txt'
		if os.path.exists(filename) is True:
			cnt += 1
		else:
			break
	print(str(cnt) + ' files collected.')
	test_num = int(np.floor(cnt * 0.2))

	# load train files
	#print(str(cnt - test_num) + ' files for training.')
	for i in range(cnt - test_num):
		feat_file = OUTPUT + 'feat_' + author + str(i) + '.txt'
		depen_file = OUTPUT + 'depen_' + author + str(i) + '.txt'
		row = dict2row(feat_dict, read_depen(depen_file))
		list_of_train.append(row)

	# load test files
	#print(str(test_num) + ' files for testing.')
	for i in range(cnt - test_num, cnt):
		feat_file = OUTPUT + 'feat_' + author + str(i) + '.txt'
		depen_file = OUTPUT + 'depen_' + author + str(i) + '.txt'
		row = dict2row(feat_dict, read_depen(depen_file))
		list_of_test.append(row)

	return np.array(list_of_train), np.array(list_of_test)


def train():
	#author_names = ['luxun', 'zhouzuoren', 'linyutang', 'sanmao', 'wangxiaobo','liucixin', 'shitiesheng']
	author_names = ['鲁迅', '周作人', '刘慈欣', '江南']
	X_train = 0
	Y_train = 0
	X_test = 0
	Y_test = 0
	for author in author_names:
		x, x_t = make_input(author)
		#print(x)
		y = np.repeat(author_names.index(author), x.shape[0]).transpose()
		y_t = np.repeat(author_names.index(author), x_t.shape[0]).transpose()
		if type(X_train) is int:
			X_train = x
			Y_train = y
			X_test = x_t
			Y_test = y_t
		elif len(x) is not 0:
			X_train = np.vstack((X_train, x))
			X_test = np.vstack((X_test, x_t))
			Y_train = np.concatenate([Y_train, y])
			Y_test = np.concatenate([Y_test, y_t])
		else:
			continue

	print(X_train.shape, X_test.shape)
	print(Y_train.shape, Y_test.shape)
	
	print('training model...')
	from sklearn import svm
	clf = svm.SVC()
	clf.fit(X_train, Y_train)
	print('done')

	print('saving model...')
	from sklearn.externals import joblib
	joblib.dump(clf, 'trained_model.pkl')
	joblib.dump((X_test, Y_test), 'X_Y_test.dat')
	print('done')



def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def test():
	from sklearn.externals import joblib
	clf = joblib.load('trained_model.pkl')
	X_test, Y_test = joblib.load('X_Y_test.dat')

	Y_pred = clf.predict(X_test)

	from sklearn.metrics import confusion_matrix
	from sklearn.metrics import accuracy_score
	from sklearn.metrics import classification_report

	print(accuracy_score(Y_test, Y_pred))
	cnf_matrix = confusion_matrix(Y_test, Y_pred)
	print(classification_report(Y_test, Y_pred, target_names=['鲁迅', '周作人', '刘慈欣', '江南']))

	plt.figure()
	plot_confusion_matrix(cnf_matrix, classes=['鲁迅', '周作人', '刘慈欣', '江南'], title='Confusion matrix, without normalization')
	# Plot normalized confusion matrix
	plt.figure()
	plot_confusion_matrix(cnf_matrix, classes=['鲁迅', '周作人', '刘慈欣', '江南'], 
		normalize=True, title='Normalized confusion matrix')
	plt.show()


train()
test()