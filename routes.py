from flask import Flask, request, jsonify
from train import trainModel
app = Flask(__name__)
@app.route("/")
def intitiate():
    return "home"

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

responses = {
    "hello": "Hi there! How can I assist you?",
    "how are you": "I'm just a machine, but thanks for asking!",
    "bye": "Goodbye! Have a great day.",
    "how" : "this is the second version of how"
}

tokenizer = Tokenizer()
tokenizer.fit_on_texts(responses.keys())

def chatbot_response(user_input):
    user_input_seq = tokenizer.texts_to_sequences([user_input])[0]
    max_similarity = 0
    best_response = "I don't understand that."
    
    for word, response in responses.items():
        word_seq = tokenizer.texts_to_sequences([word])[0]
        similarity = len(set(user_input_seq).intersection(word_seq))
        
        if user_input == word:
            return response
        if similarity > max_similarity:
            max_similarity = similarity
            best_response = response
    
    if max_similarity == len(user_input_seq):
        return best_response
    
    return "I don't understand that."

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    response = chatbot_response(user_input.lower())
    print("Chatbot:", response)

if __name__  == "__main__":
    app.run(debug=True)

