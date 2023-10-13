import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_excel("Accessibility_500.xlsx")
data = data.dropna(subset=['Questions'])
data['Questions'] = data['Questions'].str.lower()
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['Questions'])

def chatbot_response_v3(user_input):
    user_input = user_input.lower()
    user_vector = tfidf_vectorizer.transform([user_input])
    cosine_similarities = cosine_similarity(user_vector, tfidf_matrix)
    best_match_index = cosine_similarities.argmax()
    response = data.loc[best_match_index, 'Answers']
    output = {
            "response" : response
        }
    return output
