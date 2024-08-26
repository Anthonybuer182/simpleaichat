from rich.console import Console
import time
import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
from pydantic import BaseModel, Field
import orjson
import asyncio

# response = await ai("What is the capital of California?")
ai=AIChat(console=False)
ai.load_session("chat_session.json",api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3", model="qwen-turbo")
response = ai("When was it founded?")
print("second = " +response)
