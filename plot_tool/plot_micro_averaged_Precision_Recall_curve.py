import matplotlib.pylab as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score


def plot_micro_averaged_Precision_Recall_curve(Y_test, y_score):

	# For each class
	n_classes = Y_test.shape[1]
	precision = dict()
	recall = dict()
	average_precision = dict()
	for i in range(n_classes):
	    precision[i], recall[i], _ = precision_recall_curve(Y_test[:, i],
	                                                        y_score[:, i])
	    average_precision[i] = average_precision_score(Y_test[:, i], y_score[:, i])

	# A "micro-average": quantifying score on all classes jointly
	precision["micro"], recall["micro"], _ = precision_recall_curve(Y_test.ravel(),
	    y_score.ravel())
	average_precision["micro"] = average_precision_score(Y_test, y_score,
	                                                     average="micro")
	print('Average precision score, micro-averaged over all classes: {0:0.2f}'
	      .format(average_precision["micro"]))

	plt.figure()
	plt.step(recall['micro'], precision['micro'], color='b', alpha=0.2,
	         where='post')
	plt.fill_between(recall["micro"], precision["micro"], step='post', alpha=0.2,
	                 color='b')

	plt.xlabel('Recall')
	plt.ylabel('Precision')
	plt.ylim([0.0, 1.05])
	plt.xlim([0.0, 1.0])
	plt.title(
	    'Average precision score, micro-averaged over all classes: AP={0:0.2f}'
	    .format(average_precision["micro"]))
	plt.show()
	return precision, recall, average_precision