#import sklearn
#from plot_learning_curve import *


# do some prepare work
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=0)


def train(X_train, Y_train, learner):

	print('start training...')
	learner.fit(X_train, Y_train)
	return learner
	#plot_learning_curve(learner, title, X_train, Y_train, cv=5, n_jobs=4)
	#plt.show()


def test(Y_pred, Y_test, class_names=None):

	if class_names is not None:
		class_cnt_list = [x for x in range(len(class_names))]

	from sklearn.metrics import accuracy_score
	accuracy = accuracy_score(Y_test, Y_pred)

	#from plot_precision_recall_curve import plot_precision_recall_curve
	#precision, recall = plot_precision_recall_curve(Y_test, Y_pred)
	
	# multi-class
	from sklearn.preprocessing import label_binarize
	Y_test_m = label_binarize(Y_test, classes=class_cnt_list)
	Y_pred_m = label_binarize(Y_pred, classes=class_cnt_list)

	from plot_tool.plot_micro_averaged_Precision_Recall_curve import plot_micro_averaged_Precision_Recall_curve
	precision, recall, average_precision = plot_micro_averaged_Precision_Recall_curve(Y_test_m, Y_pred_m)

	from sklearn.metrics import f1_score
	f1 = f1_score(Y_test, Y_pred, average='macro')

	from sklearn.metrics import confusion_matrix
	cnf_matrix = confusion_matrix(Y_test, Y_pred)

	from plot_tool.plot_confusion_matrix import plot_confusion_matrix
	plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True, title='Normalized confusion matrix')
	
	#from plot_roc_curve import plot_roc_curve
	#plot_roc_curve(Y_test, Y_pred)

	# multi-class
	from plot_tool.multi_class_roc_curve import plot_multi_class_roc_curve
	plot_multi_class_roc_curve(Y_test_m, Y_pred_m)

	from pprint import pprint
	pprint('accuracy: ' + str(accuracy))
	pprint('f1: ' + str(f1))
	pprint('precision: ' + str(precision))
	pprint('recall: ' + str(recall))
	#print('threshold: ' + str(threshold))
