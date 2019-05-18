import json
import math
import nltk
import pickle
from datapreprocessing import textPreprocessing , createTermVector
from config import path

def read_json():
	file = open(path)
	data = json.load(file)
	return data
def calculateTFIDF(lystOfWords,QAwiseFrequency,flag):
	QADict = {}
	noOfTerms = len(lystOfWords)
	for word in lystOfWords:
		if word in QADict:
			QADict[word]+=1
		else:
			QADict[word]=1
	for word , frequency in QADict.items():
		QADict[word] = float(frequency) / noOfTerms

	tf_idfDict = {}
	for word in QADict:
		idf = calculateIDF(word,QAwiseFrequency,flag)
		tf_idfDict[word] = QADict[word] * idf
	return tf_idfDict

def return_count_of_documents_contain_specific_word(word,QAwiseFrequency,flag):
	num=0
	for cleanedQues,bigramQues,unigram_answer,question,answer in QAwiseFrequency:
		if flag == 'unigram':
			if word in cleanedQues:
				num+=1
		elif flag == 'bigram':
			s_word = (word[1],word[0]) 
			if word in bigramQues or s_word in bigramQues:
				num+=1
		elif flag == 'unigram_answer':
			if word in unigram_answer:
				num+=1

	return num

def calculateIDF(word,QAwiseFrequency,flag):
	num=return_count_of_documents_contain_specific_word(word,QAwiseFrequency,flag)
	if num > 0:
		idf = math.log(len(QAwiseFrequency)/float(num)) + 1
	else:
		idf = 1
	return idf 

def calulate_tdfidf_model():
	lystOfQA = read_json()
	QAwiseFrequency=[]

	for item in lystOfQA:
		question=item['question']
		answer = item['answer']
		cleanedQues = textPreprocessing(question)
		unigram_answer = textPreprocessing(answer)
		bigramQues = list(nltk.bigrams(cleanedQues))
		QAwiseFrequency.append((cleanedQues,bigramQues,unigram_answer,question,answer))

	data = []

	for cleanedQues, bigramQues,unigram_answer ,question , answer in QAwiseFrequency:
		dataDict={}
		tf_idf_question = calculateTFIDF(cleanedQues,QAwiseFrequency,'unigram')
		tf_idf_answer = calculateTFIDF(unigram_answer,QAwiseFrequency,'unigram_answer')
		tf_idf_question_bigram = calculateTFIDF(bigramQues,QAwiseFrequency,'bigram')
		dataDict['tf_idf_question'] = tf_idf_question
		dataDict['tf_idf_answer'] = tf_idf_answer
		dataDict['tf_idf_question_bigram'] = tf_idf_question_bigram
		dataDict['question'] = question
		dataDict['answer'] = answer
		data.append(dataDict)
	model_data = {'tf_idf':data,'QAwiseFrequency':QAwiseFrequency}
	with open('model.pickle','wb') as handle:
		pickle.dump(model_data,handle,protocol=pickle.HIGHEST_PROTOCOL)
	return "model has been saved in pickle file"

if __name__ == '__main__':
	print(calulate_tdfidf_model())


