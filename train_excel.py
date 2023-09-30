import pandas as pd

# Load the Excel data into a Pandas DataFrame
data = pd.read_excel('chatbot_data_3.xlsx')

chatbot_data = {}

for index, row in data.iterrows():
    keyword = row['Keyword']
    description = row['Descriptions']
    possible_questions = row['Possible Questions']
    answers = row['Answers']

    chatbot_data[keyword] = {
        'description': description,
        'possible_questions': possible_questions,
        'answers': answers,
    }

from fuzzywuzzy import process
def chatbot_response_v2(user_input):
    user_input = user_input.lower()

    best_match = None
    best_score = 70

    for keyword, data in chatbot_data.items():

        questions = data['possible_questions'].split(', ')
        questions.append(keyword)
        
        match, score = process.extractOne(user_input, questions)
        
        # return match,score
        if score > best_score:
            best_score = score
            best_match = keyword
    if best_match is not None:
        response = chatbot_data[best_match]['answers']
        output = {
            "response" : response
        }
        return output
    else:
        output = {
            "response" : "Chatbot: I'm sorry, I don't understand your query."
        }
        return output
