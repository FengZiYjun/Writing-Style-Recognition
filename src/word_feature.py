import nltk

def lexical_diversity(text):
    return len(set(text)) / len(text)

with open('cut.txt', encoding='utf-8') as f:
	text = f.read()


# this is the word list 
words = text.split(' \n')

# collect all word features
features = {}

features['lexical_diversity'] = lexical_diversity(words)

