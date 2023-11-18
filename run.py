from transformers import GPT2LMHeadModel, AutoTokenizer
import re
model_weights_directory = "fine-tuned-model-web-3"  

tokenizer_name = "gpt2"  

model = GPT2LMHeadModel.from_pretrained(model_weights_directory)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

def generate_answer(user_input):
    input_ids = tokenizer.encode(user_input, return_tensors="pt")

    output = model.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2)

    response = tokenizer.decode(output[0], skip_special_tokens=True)

    pattern = re.compile(r"Answer:(.*?)(?:Question:|$)", re.DOTALL)

    match = pattern.search(response)

    if match:
        answer = match.group(1).strip()
        last_sentence_index = answer.rfind('.') + 1
        answer = answer[:last_sentence_index].strip()
        response = {
            'response' : answer
        }
    else:
        response = {
            'response' : "I don't understand that!"
        }
    return response
