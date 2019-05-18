from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet
import nltk
import spacy

stopWords=set(stopwords.words('english'))
wordnet_lemmatizer=WordNetLemmatizer()
tokenizer=RegexpTokenizer(r'\w+')
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

def toLowerCase(text):

	return text.lower()

def splitSentIntoTokens(text):

	return tokenizer.tokenize(text)

def removeStopwords(wordList):

	newList = [word  for word in wordList if word not in stopWords]

	return newList

def removeSingleCharacter(wordList):

	newList = [ word  for word in wordList if len(word) != 1 ]

	return newList

def lemmatizeList(LystOfWords):

	doc = nlp(" ".join(LystOfWords))
	newList = [token.lemma_ for token in doc]

	return newList
	

def textPreprocessing(text):

	lowerCaseText = toLowerCase(text)
	tokenizedList = splitSentIntoTokens(lowerCaseText)
	listWithoutStopwords = removeStopwords(tokenizedList)
	cleanList = removeSingleCharacter(listWithoutStopwords)
	lemmatizedList = lemmatizeList(cleanList)

	return lemmatizedList

def similarWords(word='dog'):

	synonyms = []

	for syn in wordnet.synsets(word):
		for l in syn.lemmas():
			synonyms.append(l.name())

	synonyms = set(synonyms)
	newLyst = []

	for x in synonyms:
		if '_' in x:
			output = x.split()
			newLyst.extend(output)
		else:
			newLyst.append(x)

	return newLyst

def createTermVector(text):

	cleanedLyst = textPreprocessing(text)
	print(cleanedLyst)
	allRelatedWords = []

	for word,tag in nltk.pos_tag(cleanedLyst):
		if tag.startswith('NN') or tag.startswith('VB') or tag.startswith('JJ') :
			allRelatedWords.extend(similarWords(word))

	return allRelatedWords






if __name__ == "__main__":
	text = "What If my Baggage is missing at Airport ?"
	print(createTermVector(text))