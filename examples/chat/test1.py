import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
from rich.console import Console
# gpt-3.5-turbo-0125
# Ee1imTXK7hDwDM1aFa0337029aD8421bA27882E038CbA163
ai = AIChat(api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3", model="qwen-turbo",params={"temperature": 0.7},system="Write a fancy GitHub README based on the user-provided project name.")
content=ai("simpleaichat")
Console().print(f"[b]{content}[/b]: ", end="")
