import re
import codecs

#text = ""
#with codecs.open('luxunquanji.txt', encoding='utf-8') as f:
#	text = f.read()

def text_clean(text):
	print('data cleaning...')
	# 除广告
	pattern = r'(.*[WwｗＷ]{3}.*\n)|(.*[小文].*[说学].*网.*\n)|(.*[Cc][Oo][Mm].*)|(.*[Tt].?[xX].?[tT].*\n)|(.*5.*6.*\n)'
	# pattern = '(.*[WwｗＷ]{3}.*\n)|(^.*[小文].*[说学].*网.*$)'
	cleaned = re.sub(pattern, '', text)
	print('cleaned ads')

	# 除章名
	pattern2 = r'(.*第.*章.*\n)'
	cleaned = re.sub(pattern2, '', cleaned)
	print('cleaned captions')

	# 除日期
	pattern3 = r'(.*年..?月.*日\n)'
	cleaned = re.sub(pattern3, '', cleaned)
	print('cleaned dates')

	# 除其他
	pattern4 = r'(.*本篇最初发表于.*\n)'
	cleaned = re.sub(pattern4, '', cleaned)
	pattern5 = r'　　'
	cleaned = re.sub(pattern5, '', cleaned)
	pattern6 = r'    '
	pattern7 = r'	　　'
	cleaned = re.sub(pattern6, '', cleaned)
	cleaned = re.sub(pattern7, '', cleaned)

	# 分句
	endOfSentence = '。！？；：'
	# chin = '[\u4e00-\u9fa5]'

	def replacement(matchObj):
		return matchObj.group(1) + '\n' + matchObj.group(2)

	for item in endOfSentence:
		pattern = r'(' + item + ')([^\n”])'
		cleaned = re.sub(pattern, replacement, cleaned)
		#print('sub ' + item)

	cleaned = re.sub(r'([。！？]”)([^\n])', replacement, cleaned)
	#print('sub ”')
	#print(cleaned[:50])

	print('data cleaning done.')
	return cleaned


#with codecs.open('cleanluxun.txt', 'w', encoding='utf-8') as f:
#	f.write(cleaned)