import json
import math
import nltk
import pickle
from datapreprocessing import textPreprocessing , createTermVector


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

def calculate_cosine(query,question):
	dot_product = 0
	for word in query:
		if word in question:
			dot_product += query[word] * question[word]
	sum_of_sq_query = sum([query[word]**2 for word in query])
	sum_of_sq_question = sum([question[word]**2 for word in question])
	if sum_of_sq_query == 0  or sum_of_sq_question == 0:
		cosine = 0
	else:
		cosine = float(dot_product) /(math.sqrt(sum_of_sq_query) * math.sqrt(sum_of_sq_question))
	return cosine
def most_relevant_match(query):

	with open('model.pickle','rb') as handle:
		data = pickle.load(handle)

	cleanedQuery = textPreprocessing(query)
	queryTermVector = createTermVector(query)
	bigramQuery = list(nltk.bigrams(cleanedQuery))

	QAwiseFrequency=data['QAwiseFrequency']
	tf_idf_data = data['tf_idf']

	tf_idf_query = calculateTFIDF(queryTermVector,QAwiseFrequency,'unigram')
	tf_idf_query_bigram = calculateTFIDF(bigramQuery,QAwiseFrequency,'bigram')
	tf_idf_query_ans_unigram = calculateTFIDF(queryTermVector,QAwiseFrequency,'unigram_answer')

	bestScore=0
	topFourAnswer=[[0,'',''] for x in range(4)]

	for dataDict in tf_idf_data:
		tf_idf_question = dataDict['tf_idf_question']
		tf_idf_answer = dataDict['tf_idf_answer']
		tf_idf_question_bigram = dataDict['tf_idf_question_bigram']
		question = dataDict['question']
		answer = dataDict['answer']
		
		similarity_score = calculate_cosine(tf_idf_query,tf_idf_question)
		similarity_score_bigram = calculate_cosine(tf_idf_query_bigram,tf_idf_question_bigram)
		similarity_score_answer = calculate_cosine(tf_idf_query_ans_unigram,tf_idf_answer)
        
		# QUSETION -> weightage bigram : 60% and weightage unigram : 40%
		similarity_score_ques = (similarity_score * .4) + (similarity_score_bigram * .6)
		
		# ANSWER -> weightage answer : 30% and weightage question : 70%
		similarity_score = (similarity_score_answer * .25) + (similarity_score_ques * .75)


		if bestScore < similarity_score:
			bestScore=similarity_score
			response=answer
		for item in enumerate(topFourAnswer):
			index=item[0]
			if item[1][0] < similarity_score:
				topFourAnswer.insert(index,[similarity_score,question,answer])
				topFourAnswer=topFourAnswer[:4]
				break

	rating=['Most Relevant','Relevant','Less Relevant','Least Relevant']
	for item in enumerate(topFourAnswer[:]):
		if item[1][0]==0:
			topFourAnswer.remove(item[1])
			continue
		topFourAnswer[item[0]][0]=rating[item[0]]

	return topFourAnswer



if __name__ == "__main__":
	sent = "What If my Baggage is missing at Airport ?"
	sent1 = "my luggage is lost at airport ?"
	query = "reset password "
	response = most_relevant_match(query)
	print(response)