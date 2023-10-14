import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

question_embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

data = pd.read_excel("intent_500.xlsx")
tokenized_questions = [tokenizer(question, return_tensors="pt", padding=True, truncation=True, max_length=64)['input_ids'] for question in data['Questions']]

def chat_bot_response_v4(user_input):
    user_input = user_input.lower()
    user_input_tokens = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True, max_length=64)['input_ids']
    sentence_transformer = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    user_input_embedding = sentence_transformer.encode(user_input, convert_to_tensor=True)
    user_input_embedding = user_input_embedding.reshape(1, -1)
    tokenized_question_embeddings = [question_embedding_model.encode(question, convert_to_tensor=True) for question in data['Questions']]
    similarities = [cosine_similarity(user_input_embedding, question_embedding.reshape(1, -1))[0][0] for question_embedding in tokenized_question_embeddings]
    max_similarity_index = similarities.index(max(similarities))

    if max(similarities) > 0.7:
        response = data['Answers'][max_similarity_index]
    else:
        response = "I don't understand that"
        
    output = {
            "response" : response
        }
    return output
