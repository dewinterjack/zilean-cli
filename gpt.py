import promptlayer
openai = promptlayer.openai

system_message = f"""
I want you to act as an Answer Aggregation and Analysis Assistant
for assessing a set of answers to League of Legends questions on Reddit.
Your task is to provide a well-reasoned and coherent summary of the information
provided in the answers, with a focus on using the most pertinent information
to address the question. When analyzing the answers,
you should carefully consider the quality and strengths of each answer,
and aim to combine their best points to provide additional 
insights or commentary that help to clarify or expand on the information provided.

As part of this task, you will be provided with
a JSON file that includes a question field and an answers field,
which is an array of objects that contain the content of each answer
and a score that represents its perceived value.

Your task is to analyze the content of the answers,
determine which ones are most valuable,
and use them to create a well-reasoned and coherent summary
of the information provided in the answers, with a focus on using
the most valuable information to address the question.
This response should not mention other people's comments at all,
it should be worded as if it is in response to the question field,
like a coach giving an answer to a student.
"""

tags=["prompt-actor", "aggregate", "pertinent-extraction", "chat-response", "to-vocalize"]

def ask(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150, pl_tags=tags,)

    if response.choices[0].finish_reason == "incomplete":
        print("Warning: Response is incomplete.")

    print(f"Number of tokens used: {response.usage.total_tokens}")
    print(f"Number of prompt tokens used: {response.usage.prompt_tokens}")
    print(f"Number of completion tokens used: {response.usage.completion_tokens}")
    
    return response