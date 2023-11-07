import pandas as pd
import re

df = pd.read_excel('Accessibility_500.xlsx')

questions = df['Questions'].tolist()
answers = df['Answers'].tolist()















formatted_data = []
for i in range(len(questions)):
    formatted_data.append(f"Question: {questions[i]}\nAnswer: {answers[i]}\n")
with open("formatted_data.txt", "w", encoding="utf-8") as file:
    file.writelines(formatted_data)

from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

model_name = "gpt2"  
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

formatted_data_path = "formatted_data.txt"

dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=formatted_data_path,
    block_size=128,  
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,  
)

training_args = TrainingArguments(
    output_dir="./fine-tuned-model-3",  
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
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

model.save_pretrained("./fine-tuned-model-3")
