from dotenv import load_dotenv
load_dotenv()

import os
from speech_answer import get_voice
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROMPTLAYER_API_KEY = os.getenv("PROMPTLAYER_API_KEY")

from time import sleep
from rich.console import Console
from rich import print
from rich import inspect
from rich.prompt import Prompt
from rich import print

console = Console()
query = Prompt.ask("Ask Zilean a question")

import asyncio
import answers
import gpt

console = Console()

with console.status("[bold green]:crystal_ball: Asking Zilean...") as status:
    search_reddit = answers.get_comments(query)
    response = gpt.ask(search_reddit)
    inspect(response)
    console.print(search_reddit, style="bold blue")
    zilean_answer = response.choices[0].message.content
    console.print(zilean_answer, style="bold magenta")
    get_voice(zilean_answer)
    


#print(":crystal_ball: [bold magenta]Ask Zilean...[/bold magenta] :joystick:")