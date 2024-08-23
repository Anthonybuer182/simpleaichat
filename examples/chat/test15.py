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
async def main():
    response = await ai("What is the capital of California?")
    print(response)
asyncio.run(main())
