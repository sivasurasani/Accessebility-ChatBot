# import pandas as pd
# data = pd.read_excel('chatbot_data.xlsx')
# chatbot_dictionary = dict(zip(data['Key'], data['Value']))
# print(chatbot_dictionary)

# import json

# # Save the chatbot_dict to a JSON file
# with open('chatbot_data.json', 'w') as json_file:
#     json.dump(chatbot_dictionary, json_file)

import json
from flask import request
with open('chatbot_data.json', 'r') as json_file:
    chatbot_dict = json.load(json_file)

# user_input = user_input.lower() 
def chatbot_response_1(user_input):
    if user_input in chatbot_dict:
        response = chatbot_dict[user_input]
        output = {
            "response" : response
        }
        return output
    else:
        output = {
            "response" : "sorry! I don't understand that"
        }
        return output


