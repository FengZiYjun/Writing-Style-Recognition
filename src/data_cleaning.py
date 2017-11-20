import re
import codecs

#text = ""
#with codecs.open('luxunquanji.txt', encoding='utf-8') as f:
#	text = f.read()

def text_clean(text):
	print('data cleaning...')
	# 除广告
	pattern = r'(.*[WwｗＷ]{3}.*\n)|(.*[小文].*[说学].*网.*\n)|(.*[Cc][Oo][Mm].*)'
	# pattern = '(.*[WwｗＷ]{3}.*\n)|(^.*[小文].*[说学].*网.*$)'
	cleaned = re.sub(pattern, '', text)
	print('cleaned ads')
	#print(cleaned[:50])

	# 除章名
	pattern2 = r'(.*第.章.*\n)'
	cleaned = re.sub(pattern2, '', cleaned)
	print('cleaned captions')
	#print(cleaned[:50])

	# 分句
	endOfSentence = '。！？；'
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