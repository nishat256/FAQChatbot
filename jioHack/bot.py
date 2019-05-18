from config import topics
from train import read_json
from main import queryDataBase
from textSimilarity import most_relevant_match


def get_answer(topics,query):
    key_found = []
    for key, value in topics.items():
        if key == query:
            key_found.append(value)
        elif isinstance(value, dict):
            results = get_answer(value, query)
            for result in results:
                key_found.append(result)
    return key_found

def return_answer(query):
	QnAdata = read_json()
	response = []
	flag = True
	x = get_answer(topics, query)
	if x==[0] or x==[]:
		for i in QnAdata:
			if query == i['topic']:
				response.append(i["question"])
			if query == i['question']:
				response.append(i["answer"])
				flag = False
				break
	else:
		for item in x:
			response = list(item.keys())
	return (response,flag)

def botBrain(text,source):
	flag = True
	if source=="button":
		response,flag = return_answer(text)
		if flag == False:
			return (['issue resolved?','still facing issue?'],response)
		else:
			return (response,['Please select from list of questions'])

	elif source=="textField":
		optionTuple=topics.keys()
		response=queryDataBase(text)
		if not response:
			result=most_relevant_match(text)
			print(result)
			if not result:
				answer=["Sorry,I don't have answer for your query","Do you want to connect with live agent?","select option from right panel"]
				return(['Yes,I want to connect with live agent',"No,I don't want to connect with live agent"],answer)
			else:
				result=result[0][2]
				answer=[result]

				return(['issue resolved?','still facing issue?'],answer)
		else:
			bot_answer=[response[0]]

		return (optionTuple,bot_answer)

if __name__ == "__main__":
	print(get_answer(topics,'Baggage'))
