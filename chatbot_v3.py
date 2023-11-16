import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_excel("web_accessibility_data.xlsx")
data = data.dropna(subset=['Questions'])
data['Questions'] = data['Questions'].str.lower()
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['Questions'])
import re
def chatbot_response_v3(user_input):
    user_input = user_input.lower()
    user_input = re.sub(r'[!?]', '', user_input)
    if(user_input in ('hi', 'hello')):
        output = {
            "response" : 'Hello! How can I help you?'
        }
    elif(user_input in ('how are you')):
        output = {
            "response" : 'Hello! I am fine! How can I help you?'
        }
    elif(user_input in ('who are you')):
        output = {
            "response" : 'I am an accessibility chatbot and I am here to help with mobile accessibility guidelines'
        }
    else:
        user_vector = tfidf_vectorizer.transform([user_input])
        cosine_similarities = cosine_similarity(user_vector, tfidf_matrix)
        best_match_index = cosine_similarities.argmax()
        response = data.loc[best_match_index, 'Answers']
        if(':' in response):
            response_split = response.split(":", 1)
            response = response_split[1]
        if((cosine_similarities[0][best_match_index] * 100) > 0.5):
            output = {
                "response" : response.strip()
            }
        else:
           return extractCommonMessage()
    return output


def extractCommonMessage():
    output = {
        "response" : "I don't Undestand that!"
    }
    return output