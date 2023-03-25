from dotenv import load_dotenv
load_dotenv()

import os
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
    console.print(response.choices[0].message.content, style="bold magenta")


#print(":crystal_ball: [bold magenta]Ask Zilean...[/bold magenta] :joystick:")