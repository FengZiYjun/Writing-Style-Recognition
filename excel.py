import xlsxwriter

PATH = './output/'

def save_dict(dictionary, filename):
	workbook = xlsxwriter.Workbook(PATH + filename + '.csv')
	worksheet = workbook.add_worksheet()
	row = 0
	for key in dictionary:
		worksheet.write(row, 0, key)
		if type(dictionary[key]) is list:
			col = 1
			for item in dictionary[key]:
				worksheet.write(row, col, item)
				col += 1
		else:
			worksheet.write(row, 1, dictionary[key])
		row += 1
	workbook.close()

def save_table(table, col_labels=None, row_labels=None, filename='default'):
	# table ---- 2-D list
	workbook = xlsxwriter.Workbook(PATH + filename + '.csv')
	worksheet = workbook.add_worksheet()
	for c in range(len(col_labels)):
		worksheet.write(0, c+1, col_labels[c])
	r = 1
	for row in table:
		worksheet.write(r, 0, row_labels[r-1])
		c = 1
		for item in row:
			worksheet.write(r, c, item)
			c += 1
		r += 1
	workbook.close()