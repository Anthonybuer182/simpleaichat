import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union
import orjson
from simpleaichat.simpleaichat.utils import fd
from uuid import uuid4
# gpt-3.5-turbo-0125
# Ee1imTXK7hDwDM1aFa0337029aD8421bA27882E038CbA163

model="qwen-turbo"
api_key= "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3"

system_optimized = """Write a Python function based on the user input.

You must obey ALL the following rules:
- Only respond with the Python function.
- Never put in-line comments or docstrings in your code."""

params = {"temperature": 0.0}  # for reproducibility

ai = AIChat(
    api_key=api_key,
    console=False,
    save_messages=False,  # with schema I/O, messages are never saved
    model=model,
)

ai_func = AIChat(api_key=api_key, console=False)
def gen_code(query):
    id = uuid4()
    ai_func.new_session(api_key=api_key, id=id, system=system_optimized, params=params, model=model)
    _ = ai_func(query, id=id)
    response_optimized = ai_func("Make it more efficient.", id=id)

    ai_func.delete_session(id=id)
    return response_optimized
code = gen_code("is_palindrome")
print(code)
print("\n\n")