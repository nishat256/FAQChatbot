from tinydb import TinyDB, Query
from datapreprocessing import textPreprocessing
import nltk
db = TinyDB('db.json')

def queryDataBase(text):
	resp=db.all()
	uniPlusBimax=0
	uniMax=0
	bigramMax=0
	biAnswer=None
	uniAnswer=None
	queryUni=textPreprocessing(text)
	queryBi = list(nltk.bigrams(queryUni))
	for item in resp:
		questionUni=textPreprocessing(item['Question'])
		questionBi = list(nltk.bigrams(questionUni))
		wordMatched=0
		for word in queryUni:
			if word in questionUni:
				wordMatched+=1
		bigramMatched=0
		for bigram in queryBi:
			if bigram in questionBi:
				bigramMatched+=1
		per=float(wordMatched)/len(queryUni)
		if uniPlusBimax < per and bigramMax <= bigramMatched:
			uniPlusBimax = per
			bigramMax = bigramMatched
			biAnswer = item['Answer']
	if bigramMax >= 1 and uniPlusBimax >= .6: 
		return (biAnswer,uniPlusBimax)
	else:
		return False