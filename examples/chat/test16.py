import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
from pydantic import BaseModel, Field
import orjson
from getpass import getpass
import asyncio
from rich.console import Console
import time
model="qwen-turbo"
api_key= "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3"
ai = AsyncAIChat(api_key=api_key, console=False,model = model)  # for reproducibility
# response = await ai("What is the capital of California?")
states = ["Washington", "New Mexico", "Texas", "Mississippi", "Alaska"]

ai_2 = AsyncAIChat(api_key=api_key, console=False)
for state in states:
    ai_2.new_session(api_key=api_key, id=state, model = model)
tasks = []
for state in states:
    tasks.append(ai_2(f"What is the capital of {state}?", id=state))

async def main():
    results = await asyncio.gather(*tasks)
    print(results)
asyncio.run(main())
