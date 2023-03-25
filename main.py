from dotenv import load_dotenv
load_dotenv()

import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROMPTLAYER_API_KEY = os.getenv("PROMPTLAYER_API_KEY")

import answers
answers = answers.get_comments("Is Liandrys good on zilean")
print("Answers \n" + answers)

import gpt
ask = gpt.ask(answers)

print(ask.choices[0].message.content)
