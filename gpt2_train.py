import pandas as pd
import re

df = pd.read_excel('web_accessibility_data.xlsx')


questions = df['Questions'].tolist()
answers = df['Answers'].tolist()

questions = [str(question).strip() if pd.notna(question) else '' for question in questions]

answers = [str(answer).strip() if pd.notna(answer) else '' for answer in answers]

formatted_data = []
for i in range(len(questions)):
    formatted_data.append(f"Question: {questions[i]}\nAnswer: {answers[i]}\n")
with open("formatted_data_web-3.txt", "w", encoding="utf-8") as file:
    file.writelines(formatted_data)

from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

model_name = "gpt2"  
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

formatted_data_path = "formatted_data_web-3.txt"

dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=formatted_data_path,
    block_size=256,  
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,  
)

training_args = TrainingArguments(
    output_dir="./fine-tuned-model-web-3",  
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=8,
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

trainer.train()

model.save_pretrained("./fine-tuned-model-web-3")
